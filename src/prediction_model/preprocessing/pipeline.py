"""
GridGuard AI — Production Preprocessing Pipeline & Transformers.
Implements DomainOutlierClipper, Scikit-learn ColumnTransformer, and
the master GridGuardPreprocessingPipeline orchestrator.
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

from preprocessing.validation import DataValidator
from preprocessing.feature_engineering import TemporalFeatureEngineer

class DomainOutlierClipper(BaseEstimator, TransformerMixin):
    def __init__(self, lower_percentile: float = 0.2, upper_percentile: float = 99.8):
        self.lower_percentile = lower_percentile
        self.upper_percentile = upper_percentile
        self.bounds_: Dict[str, Tuple[float, float]] = {}

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "DomainOutlierClipper":
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            series = X[col].dropna()
            if len(series) > 0:
                low = float(np.percentile(series, self.lower_percentile))
                high = float(np.percentile(series, self.upper_percentile))
                self.bounds_[col] = (low, high)
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        clipped = X.copy()
        for col, (low, high) in self.bounds_.items():
            if col in clipped.columns:
                clipped[col] = clipped[col].clip(lower=low, upper=high)
        return clipped

def build_sklearn_preprocessor(
    numerical_features: List[str],
    categorical_features: List[str]
) -> ColumnTransformer:
    num_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", RobustScaler())
    ])
    
    cat_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipe, numerical_features),
            ("cat", cat_pipe, categorical_features)
        ],
        remainder="drop"
    )
    return preprocessor

class GridGuardPreprocessingPipeline(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        sampling_interval_hours: int = 4,
        artifacts_dir: Optional[Path] = None
    ):
        self.sampling_interval_hours = sampling_interval_hours
        self.artifacts_dir = Path(artifacts_dir) if artifacts_dir else Path("artifacts")
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        
        self.validator = DataValidator()
        self.feature_engineer = TemporalFeatureEngineer(sampling_interval_hours=sampling_interval_hours)
        self.outlier_clipper = DomainOutlierClipper()
        self.preprocessor: Optional[ColumnTransformer] = None
        
        self.numerical_features_: List[str] = []
        self.categorical_features_: List[str] = ["asset_type", "location"]
        self.transformed_feature_names_: List[str] = []
        self.is_fitted_: bool = False

    def fit(self, X_train: pd.DataFrame, y_train: Optional[pd.Series] = None) -> "GridGuardPreprocessingPipeline":
        if y_train is not None:
            y_train = pd.Series(y_train).reset_index(drop=True)
        cleaned = self.validator.sanitize(X_train)
        
        self.feature_engineer.fit(cleaned, y_train)
        engineered = self.feature_engineer.transform(cleaned)
        
        self.outlier_clipper.fit(engineered)
        clipped = self.outlier_clipper.transform(engineered)
        
        exclude_cols = ["timestamp", "asset_id", "failure_within_horizon"] + self.categorical_features_
        self.numerical_features_ = [
            c for c in clipped.select_dtypes(include=[np.number]).columns if c not in exclude_cols
        ]
        
        self.preprocessor = build_sklearn_preprocessor(
            self.numerical_features_, self.categorical_features_
        )
        self.preprocessor.fit(clipped)
        
        cat_encoder = self.preprocessor.named_transformers_["cat"].named_steps["encoder"]
        cat_names_out = list(cat_encoder.get_feature_names_out(self.categorical_features_))
        self.transformed_feature_names_ = self.numerical_features_ + cat_names_out
        
        self.is_fitted_ = True
        return self

    def transform(self, X: pd.DataFrame) -> Tuple[np.ndarray, pd.DataFrame]:
        if not self.is_fitted_ or self.preprocessor is None:
            raise RuntimeError("Pipeline must be fitted before transform.")
            
        cleaned = self.validator.sanitize(X, drop_duplicates=False)
        engineered = self.feature_engineer.transform(cleaned)
        clipped = self.outlier_clipper.transform(engineered)
        
        X_trans = self.preprocessor.transform(clipped)
        df_trans = pd.DataFrame(X_trans, columns=self.transformed_feature_names_)
        return X_trans, df_trans

    def fit_transform(self, X_train: pd.DataFrame, y_train: Optional[pd.Series] = None) -> Tuple[np.ndarray, pd.DataFrame]:
        return self.fit(X_train, y_train).transform(X_train)

    def save(self, filepath: Optional[Path] = None) -> Path:
        if not self.is_fitted_:
            raise RuntimeError("Cannot save unfitted pipeline.")
        save_path = Path(filepath) if filepath else self.artifacts_dir / "fitted_preprocessing_pipeline.joblib"
        save_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, save_path)
        print(f"Fitted preprocessing pipeline successfully saved to: {save_path}")
        return save_path

    @classmethod
    def load(cls, filepath: Path) -> "GridGuardPreprocessingPipeline":
        return joblib.load(filepath)

# Backward-compatible alias
build_preprocessing_pipeline = build_sklearn_preprocessor
