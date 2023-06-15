# stdlib
from typing import Any, List

# third party
import pandas as pd
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

# adjutorium absolute
import adjutorium.plugins.core.params as params
import adjutorium.plugins.prediction.classifiers.base as base
from adjutorium.plugins.prediction.classifiers.helper_calibration import (
    calibrated_model,
)
import adjutorium.utils.serialization as serialization


class QuadraticDiscriminantAnalysisPlugin(base.ClassifierPlugin):
    """Classification plugin based on Quadratic Discriminant Analysis.

    Method:
        The plugin is based on Quadratic Discriminant Analysis, a classifier with a quadratic decision boundary, generated by fitting class conditional densities to the data and using Bayes’ rule.

    Example:
        >>> from adjutorium.plugins.prediction import Predictions
        >>> plugin = Predictions(category="classifiers").get("qda")
        >>> from sklearn.datasets import load_iris
        >>> X, y = load_iris(return_X_y=True)
        >>> plugin.fit_predict(X, y) # returns the probabilities for each class
    """

    def __init__(self, calibration: int = 0, model: Any = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if model is not None:
            self.model = model
            return

        model = QuadraticDiscriminantAnalysis()
        self.model = calibrated_model(model, calibration)

    @staticmethod
    def name() -> str:
        return "qda"

    @staticmethod
    def hyperparameter_space(*args: Any, **kwargs: Any) -> List[params.Params]:
        return []

    def _fit(
        self, X: pd.DataFrame, *args: Any, **kwargs: Any
    ) -> "QuadraticDiscriminantAnalysisPlugin":
        self.model.fit(X, *args, **kwargs)
        return self

    def _predict(self, X: pd.DataFrame, *args: Any, **kwargs: Any) -> pd.DataFrame:
        return self.model.predict(X, *args, **kwargs)

    def _predict_proba(
        self, X: pd.DataFrame, *args: Any, **kwargs: Any
    ) -> pd.DataFrame:
        return self.model.predict_proba(X, *args, **kwargs)

    def save(self) -> bytes:
        return serialization.save_model(self.model)

    @classmethod
    def load(cls, buff: bytes) -> "QuadraticDiscriminantAnalysisPlugin":
        model = serialization.load_model(buff)

        return cls(model=model)


plugin = QuadraticDiscriminantAnalysisPlugin
