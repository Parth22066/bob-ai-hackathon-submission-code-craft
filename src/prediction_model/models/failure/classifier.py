"""
Supervised failure prediction model.
Implements XGBoost and Random Forest classifiers with built-in imbalance handling and preprocessing.
SRS FR-08 and Section 6.
"""

from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer

from models.base import BasePredictor
from preprocessing.pipeline import build_preprocessing_pipeline
from features.builder import NUMERICAL_FEATURE_NAMES, CATEGORICAL_FEATURE_NAMES

class EquipmentFailureClassifier(BasePredictor):
    def __init__(
        self,
        model_type: str = "xgboost",
        random_state: int = 42,
        numerical_features: Optional[List[str]] = None,
        categorical_features: Optional[List[str]] = None,
        **kwargs
    ):
        self.model_type = model_type.lower()
        self.random_state = random_state
        self.numerical_features = numerical_features or NUMERICAL_FEATURE_NAMES
        self.categorical_features = categorical_features or CATEGORICAL_FEATURE_NAMES
        self.kwargs = kwargs
        
        self.preprocessor: Optional[ColumnTransformer] = None
        self.model = None
        self.feature_names_out: List[str] = []

    def fit(self, X: pd.DataFrame, y: pd.Series) -> "EquipmentFailureClassifier":
        # 1. Fit Preprocessing Pipeline
        self.preprocessor = build_preprocessing_pipeline(
            self.numerical_features, self.categorical_features
        )
        X_trans = self.preprocessor.fit_transform(X)
        
        # Save output feature names for explainability
        cat_encoder = self.preprocessor.named_transformers_["cat"].named_steps["encoder"]
        cat_features_out = list(cat_encoder.get_feature_names_out(self.categorical_features))
        self.feature_names_out = self.numerical_features + cat_features_out
        
        # 2. Compute Imbalance Ratio
        num_neg = int((y == 0).sum())
        num_pos = int((y == 1).sum())
        scale_pos_weight = max(1.0, float(num_neg / max(1, num_pos)))
        
        # 3. Instantiate and Fit Model
        if self.model_type == "xgboost":
            default_xgb = {
                "n_estimators": 200,
                "max_depth": 4,
                "learning_rate": 0.05,
                "subsample": 0.8,
                "colsample_bytree": 0.8,
                "scale_pos_weight": scale_pos_weight,
                "random_state": self.random_state,
                "eval_metric": "logloss",
                "n_jobs": -1
            }
            default_xgb.update(self.kwargs)
            self.model = XGBClassifier(**default_xgb)
        elif self.model_type == "random_forest":
            default_rf = {
                "n_estimators": 200,
                "max_depth": 8,
                "class_weight": "balanced_subsample",
                "random_state": self.random_state,
                "n_jobs": -1
            }
            default_rf.update(self.kwargs)
            self.model = RandomForestClassifier(**default_rf)
        else:
            raise ValueError(f"Unsupported model_type: {self.model_type}")
            
        self.model.fit(X_trans, y)
        return self

    def predict(self, X: pd.DataFrame, threshold: float = 0.5) -> np.ndarray:
        probas = self.predict_proba(X)
        return (probas >= threshold).astype(int)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Returns P(failure=1)."""
        if self.preprocessor is None or self.model is None:
            raise RuntimeError("Model must be fitted before predict_proba.")
        X_trans = self.preprocessor.transform(X)
        return self.model.predict_proba(X_trans)[:, 1]

    def get_feature_importances(self) -> Dict[str, float]:
        """Returns sorted feature importances."""
        if self.model is None:
            return {}
        raw_imp = self.model.feature_importances_
        imp_dict = dict(zip(self.feature_names_out, [float(v) for v in raw_imp]))
        return dict(sorted(imp_dict.items(), key=lambda item: item[1], reverse=True))
