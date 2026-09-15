"""
Probability calibration module for equipment failure predictions.
Calibrates model scores to true empirical failure frequencies.
"""

from typing import Optional
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import brier_score_loss

from models.failure.classifier import EquipmentFailureClassifier
from models.base import BasePredictor

class CalibratedFailureModel(BasePredictor):
    def __init__(
        self,
        base_classifier: EquipmentFailureClassifier,
        method: str = "sigmoid",
        cv: int = 3
    ):
        self.base_classifier = base_classifier
        self.method = method
        self.cv = cv
        self.calibrated_model: Optional[CalibratedClassifierCV] = None

    def fit(self, X: pd.DataFrame, y: pd.Series) -> "CalibratedFailureModel":
        """
        Fits base preprocessor, trains base model for importances,
        and trains CalibratedClassifierCV for calibrated probabilities.
        """
        # 1. Fit base classifier (fits preprocessor and underlying model)
        self.base_classifier.fit(X, y)
        
        # 2. Extract transformed features
        X_trans = self.base_classifier.preprocessor.transform(X)
        
        # Determine valid CV folds given class counts
        pos_count = int((y == 1).sum())
        cv_folds = min(self.cv, max(2, pos_count))
        
        # 3. Fit CalibratedClassifierCV using internal cross-validation
        self.calibrated_model = CalibratedClassifierCV(
            estimator=self.base_classifier.model,
            method=self.method,
            cv=cv_folds
        )
        self.calibrated_model.fit(X_trans, y)
        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Returns calibrated probability P(failure=1)."""
        if self.calibrated_model is None or self.base_classifier.preprocessor is None:
            raise RuntimeError("Model must be fitted before predict_proba.")
        X_trans = self.base_classifier.preprocessor.transform(X)
        return self.calibrated_model.predict_proba(X_trans)[:, 1]

    def predict(self, X: pd.DataFrame, threshold: float = 0.5) -> np.ndarray:
        probas = self.predict_proba(X)
        return (probas >= threshold).astype(int)

    def evaluate_calibration(self, X: pd.DataFrame, y: pd.Series) -> float:
        """Computes Brier Score (lower is better, 0.0 is perfect)."""
        probas = self.predict_proba(X)
        return float(brier_score_loss(y, probas))
