from typing import Literal

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, MultiOutputMixin


class SingleDecisionTree(BaseEstimator, ClassifierMixin, MultiOutputMixin):
    def __init__(
        self,
        threshold_margin: float,
        threshold_step: float,
        ensemble_num_trees: int | None,
        ensemble_percentile_gap: float | None,
        quantile_based: bool = True,
        aggregate_func: Literal["sum", "sharpe"] = "sharpe",
    ):
        assert threshold_margin < 0.5, f"Margin too large: {threshold_margin}"
        assert threshold_step < 0.2, f"Step too large: {threshold_margin}"

        self.threshold_to_test = np.arange(
            threshold_margin, 1 - threshold_margin, threshold_step
        ).tolist()
        self.quantile_based = quantile_based
        self.ensemble_num_trees = ensemble_num_trees
        self.ensemble_percentile_gap = ensemble_percentile_gap
        self.aggregate_func = aggregate_func
        if self.ensemble_num_trees is not None:
            assert self.ensemble_percentile_gap is not None, "Percentile gap required"

    def fit(
        self, X: pd.DataFrame, y: pd.Series, sample_weight: pd.Series | None = None
    ):
        assert X.shape[1] == 1, "Only single feature supported"
        X = X.squeeze()
        if isinstance(X, pd.Series):
            X = X.to_numpy()
        if isinstance(y, pd.Series):
            y = y.to_numpy()
        splits = (
            np.quantile(X, self.threshold_to_test, axis=0, method="closest_observation")
            if self.quantile_based
            else (self.threshold_to_test * (y.max() - y.min()) + y.min())
        )
        splits = np.unique(splits)
        if len(splits) == 1:
            self._best_split = splits[0]
            self._all_splits = [splits[0]]
            self._positive_class = 1
            return
        if len(splits) == 2:
            self._best_split = splits[0] - ((splits[1] - splits[0]) / 2)
            self._all_splits = [splits[0], splits[1]]
            self._positive_class = np.argmax(
                [np.mean(y[self._best_split > X]), np.mean(y[self._best_split <= X])]
            )
            return

        differences = [
            calculate_bin_diff(t, X=X, y=y, agg_method=self.aggregate_func)
            for t in splits
        ]
        self._best_split = float(splits[np.argmax(np.abs(differences))])
        self._all_splits = (
            _generate_neighbouring_splits(
                threshold=self.threshold_to_test[np.argmax(np.abs(differences))],
                num_trees=self.ensemble_num_trees,
                percentile_gap=self.ensemble_percentile_gap,  # type: ignore
                X=X,
            )
            if self.ensemble_num_trees is not None
            else [self._best_split]
        )
        self._positive_class = int(
            np.argmax(
                [np.mean(y[self._best_split > X]), np.mean(y[self._best_split <= X])]
            )
        )

    def predict(self, X: pd.DataFrame) -> pd.Series:
        assert self._best_split is not None, "Model not fitted"
        assert self._positive_class is not None, "Model not fitted"
        assert self._all_splits is not None, "Model not fitted"
        other_class = 1 - self._positive_class
        return pd.Series(
            np.array(
                [
                    np.where(X.squeeze() > split, self._positive_class, other_class)
                    for split in self._all_splits
                ]
            ).mean(axis=0),
            index=X.index,
        )


def _generate_neighbouring_splits(
    threshold: float, num_trees: int, percentile_gap: float, X: np.ndarray
) -> list[float]:
    thresholds = [threshold - percentile_gap, threshold, threshold + percentile_gap]
    if num_trees == 5:
        thresholds = [
            threshold - 2 * percentile_gap,
            threshold - percentile_gap,
            threshold,
            threshold + percentile_gap,
            threshold + 2 * percentile_gap,
        ]
    if num_trees == 7:
        thresholds = [
            threshold - 3 * percentile_gap,
            threshold - 2 * percentile_gap,
            threshold - percentile_gap,
            threshold,
            threshold + percentile_gap,
            threshold + 2 * percentile_gap,
            threshold + 3 * percentile_gap,
        ]
    if num_trees == 9:
        thresholds = [
            threshold - 4 * percentile_gap,
            threshold - 3 * percentile_gap,
            threshold - 2 * percentile_gap,
            threshold - percentile_gap,
            threshold,
            threshold + percentile_gap,
            threshold + 2 * percentile_gap,
            threshold + 3 * percentile_gap,
            threshold + 4 * percentile_gap,
        ]
    return [
        float(np.quantile(X, threshold, axis=0, method="closest_observation"))
        for threshold in thresholds
    ]


class RegularizedDecisionTree(BaseEstimator, ClassifierMixin, MultiOutputMixin):
    def __init__(
        self,
        threshold_margin: float,
        threshold_step: float,
        num_splits: int = 4,
        aggregate_func: Literal["mean", "sharpe"] = "sharpe",
    ):
        self.aggregate_func = aggregate_func
        assert threshold_margin <= 0.15, f"Margin too large: {threshold_margin}"
        assert threshold_step <= 0.05, f"Step too large: {threshold_margin}"
        self.num_splits = num_splits
        if threshold_margin > 0:
            threshold_margin = 0.5 - threshold_margin

            self.threshold_to_test = (
                np.arange(
                    threshold_margin, 1 - threshold_margin + 0.0001, threshold_step
                )
                .round(3)
                .tolist()
            )
        else:
            self.threshold_to_test = [0.5]

    def fit(
        self, X: pd.DataFrame, y: pd.Series, sample_weight: pd.Series | None = None
    ):
        assert X.shape[1] == 1, "Only single feature supported"
        X = X.squeeze()
        splits = np.quantile(
            X, self.threshold_to_test, axis=0, method="closest_observation"
        )

        if isinstance(X, pd.Series):
            X = X.to_numpy()
        if isinstance(y, pd.Series):
            y = y.to_numpy()
        differences = [
            calculate_bin_diff(t, X=X, y=y, agg_method=self.aggregate_func)
            for t in splits
        ]
        idx_best_split = np.argmax(np.abs(differences))
        best_split = float(splits[idx_best_split])
        if np.isnan(best_split):
            self._splits = [splits[1]]
            self._positive_class = 1
            return

        self._positive_class = int(
            np.argmax(
                [
                    y[best_split > X].sum(),
                    y[best_split <= X].sum(),
                ]
            )
        )
        best_quantile = self.threshold_to_test[idx_best_split]
        deciles_to_split = (
            list(
                reversed(
                    [
                        best_quantile - (i * 0.01)
                        for i in range(0, 6 * self.num_splits, 5)
                    ][1:]
                )
            )
            + [best_quantile]
            + [best_quantile + (i * 0.01) for i in range(0, 6 * self.num_splits, 5)][1:]
        )
        self._splits = np.quantile(
            X,
            [round(i, 2) for i in deciles_to_split],
            axis=0,
            method="nearest",
        )
        assert np.isnan(self._splits).sum() == 0

    def predict(self, X: pd.DataFrame) -> pd.Series:
        assert self._positive_class is not None, "Model not fitted"
        assert self._splits is not None, "Model not fitted"

        output = np.searchsorted(self._splits, X.squeeze(), side="right") / len(
            self._splits
        )
        if isinstance(X, pd.DataFrame):
            output = pd.Series(output, index=X.index)
        if self._positive_class == 0:
            output = 1 - output
        return output


class UltraRegularizedDecisionTree(BaseEstimator, ClassifierMixin, MultiOutputMixin):
    def __init__(
        self,
        threshold_margin: float,  # used to produce the range of deciles/percentiles when the model can split, 0.1 means the range is 0.4 to 0.6 percentile.
        threshold_step: float,  # used to produce the range of deciles/percentiles when the model can split, 0.05 means the possible splits will be spaced 5% apart
        positive_class: int,  # this model can not flip the "coefficient", so the positive class is fixed
        num_splits: int = 4,  # number of extra splits to make around the best split, eg. if 2 and the best quantile is 0.5, then the splits will be [0.45, 0.5, 0.55]
        aggregate_func: Literal["mean", "sharpe"] = "sharpe",
    ):
        self.aggregate_func = aggregate_func
        assert threshold_margin <= 0.3, f"Margin too large: {threshold_margin}"
        assert threshold_step <= 0.05, f"Step too large: {threshold_margin}"
        self.num_splits = num_splits
        self.positive_class = positive_class
        if threshold_margin > 0:
            threshold_margin = 0.5 - threshold_margin

            self.threshold_to_test = (
                np.arange(
                    threshold_margin, 1 - threshold_margin + 0.0001, threshold_step
                )
                .round(3)
                .tolist()
            )
        else:
            self.threshold_to_test = [0.5]

    def fit(
        self, X: pd.DataFrame, y: pd.Series, sample_weight: pd.Series | None = None
    ):
        assert X.shape[1] == 1, "Only single feature supported"
        X = X.squeeze()
        splits = np.quantile(
            X, self.threshold_to_test, axis=0, method="closest_observation"
        )
        if isinstance(X, pd.Series):
            X = X.to_numpy()
        if isinstance(y, pd.Series):
            y = y.to_numpy()
        differences = [
            calculate_bin_diff(t, X=X, y=y, agg_method=self.aggregate_func)
            for t in splits
        ]
        idx_best_split = np.argmax(np.abs(differences))
        best_split = float(splits[idx_best_split])
        if np.isnan(best_split):
            self._splits = [splits[1]]
            return

        best_quantile = self.threshold_to_test[idx_best_split]
        deciles_to_split = (
            list(
                reversed(
                    [
                        best_quantile - (i * 0.01)
                        for i in range(0, 6 * self.num_splits, 5)
                    ][1:]
                )
            )
            + [best_quantile]
            + [best_quantile + (i * 0.01) for i in range(0, 6 * self.num_splits, 5)][1:]
        )  # number of extra splits to make around the best split, eg. if 2 and the best quantile is 0.5, then the splits will be [0.45, 0.5, 0.55]
        self._splits = np.quantile(
            X,
            [round(i, 2) for i in deciles_to_split],
            axis=0,
            method="nearest",
        )  # translate the percentiles into actual values
        assert np.isnan(self._splits).sum() == 0

    def predict(self, X: pd.DataFrame) -> pd.Series:
        assert self.positive_class is not None, "Model not fitted"
        assert self._splits is not None, "Model not fitted"

        output = (
            np.searchsorted(self._splits, X.squeeze(), side="right") / len(self._splits)
        )  # find the value in the splits, the index of the split acts as a scaled value between 0 and 1
        if isinstance(X, pd.DataFrame):
            output = pd.Series(output, index=X.index)
        if self.positive_class == 0:
            output = 1 - output
        return output


def calculate_bin_diff(
    quantile: float,
    X: np.ndarray,
    y: np.ndarray,
    agg_method: Literal["mean", "sharpe"],
) -> float:
    above = quantile > X

    agg = np.array([np_mean(y[~above]), np_mean(y[above])])
    if agg_method == "sharpe":
        agg = agg / np.array([np_std(y[~above]), np_std(y[above])])
    if len(agg) == 0:
        return 0.0
    if len(agg) == 1:
        return 0.0
    if len(agg) > 2:
        raise AssertionError("Too many bins")
    return np.diff(agg)[0]


def np_mean(x):
    if x.size == 0:
        return 0.0
    return x.mean()


def np_std(x):
    if x.size == 0:
        return 0.0
    return x.std()
