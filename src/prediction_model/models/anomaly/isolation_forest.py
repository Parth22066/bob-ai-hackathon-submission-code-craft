"""
Unsupervised Sensor Anomaly Detector using Isolation Forest.
Implements SRS FR-09 and Section 6.
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import RobustScaler
from models.base import BasePredictor

ANOMALY_SENSOR_COLUMNS = [
    "temperature_c",
    "vibration_mms",
    "partial_discharge_pc",
    "oil_quality_index",
    "load_current_a",
    "voltage_deviation_pct"
]

class SensorAnomalyDetector(BasePredictor):
    def __init__(
        self,
        contamination: float = 0.05,
        n_estimators: int = 150,
        random_state: int = 42,
        sensor_columns: Optional[List[str]] = None
    ):
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.sensor_columns = sensor_columns or ANOMALY_SENSOR_COLUMNS
        
        self.scaler = RobustScaler()
        self.model = IsolationForest(
            contamination=self.contamination,
            n_estimators=self.n_estimators,
            random_state=self.random_state,
            n_jobs=-1
        )
        self.baseline_stats: Dict[str, Dict[str, float]] = {}
        self.threshold: float = 0.0

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "SensorAnomalyDetector":
        """
        Fits scaler and Isolation Forest on baseline sensor telemetry.
        """
        X_sub = X[self.sensor_columns].copy()
        
        # Calculate baseline statistics for anomaly explanation
        for col in self.sensor_columns:
            self.baseline_stats[col] = {
                "mean": float(X_sub[col].mean()),
                "std": float(X_sub[col].std() + 1e-6),
                "q25": float(X_sub[col].quantile(0.25)),
                "q75": float(X_sub[col].quantile(0.75))
            }
            
        X_scaled = self.scaler.fit_transform(X_sub)
        self.model.fit(X_scaled)
        
        # Determine empirical decision threshold (5th percentile of decision function)
        raw_scores = self.model.decision_function(X_scaled)
        self.threshold = float(np.percentile(raw_scores, self.contamination * 100))
        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Returns binary flag: 1 for anomaly, 0 for normal."""
        scores = self.predict_anomaly_severity(X)
        return (scores >= 0.5).astype(int)

    def predict_anomaly_severity(self, X: pd.DataFrame) -> np.ndarray:
        """
        Returns normalized anomaly severity S_anomaly in [0.0, 1.0].
        0.0 = completely normal, 1.0 = extreme anomaly.
        """
        X_sub = X[self.sensor_columns].copy()
        X_scaled = self.scaler.transform(X_sub)
        raw_scores = self.model.decision_function(X_scaled) # lower = more anomalous
        
        # Map raw score to [0, 1] severity
        # Points below threshold map to > 0.5 severity
        severity = 1.0 / (1.0 + np.exp(8.0 * (raw_scores - self.threshold)))
        return np.clip(severity, 0.0, 1.0)

    def decompose_anomaly(self, sensor_reading: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Identifies which specific sensor readings deviate most from baseline normal distributions.
        Returns list of sensors sorted by z-score deviation.
        """
        deviations = []
        for col in self.sensor_columns:
            if col in sensor_reading:
                val = float(sensor_reading[col])
                mean = self.baseline_stats.get(col, {}).get("mean", val)
                std = self.baseline_stats.get(col, {}).get("std", 1.0)
                z = (val - mean) / std
                
                deviations.append({
                    "sensor": col,
                    "value": round(val, 2),
                    "baseline_mean": round(mean, 2),
                    "z_score": round(float(z), 2),
                    "is_abnormal": bool(abs(z) >= 2.5)
                })
                
        deviations.sort(key=lambda x: abs(x["z_score"]), reverse=True)
        return deviations
