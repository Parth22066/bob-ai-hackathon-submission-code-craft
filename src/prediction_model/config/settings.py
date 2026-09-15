"""
System configuration for GridGuard AI ML subsystem.
Provides configurable prediction horizon, paths, model settings, and risk score weights.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent

@dataclass
class MLConfig:
    base_dir: Path = BASE_DIR
    artifacts_dir: Path = BASE_DIR / "artifacts"
    data_dir: Path = BASE_DIR / "data"
    config_dir: Path = BASE_DIR / "config"
    
    # Prediction Horizon (Configurable as per SRS assumption)
    # Default: 168 hours (7 days)
    # Valid range: 24 to 336 hours
    prediction_horizon_hours: int = 168
    lead_time_hours: int = 2  # Anti-leakage lead buffer
    
    # Random Seed for Reproducibility
    random_state: int = 42
    
    # Risk Scoring Weights (FR-10)
    risk_weights: Dict[str, float] = field(default_factory=lambda: {
        "failure_probability": 0.35,
        "anomaly_severity": 0.20,
        "weather_risk": 0.15,
        "historical_incidents": 0.15,
        "asset_criticality": 0.15,
    })
    
    risk_thresholds: Dict[str, float] = field(default_factory=lambda: {
        "low": 35.0,
        "medium": 65.0,
        "high": 85.0,
        "critical": 100.0,
    })
    
    operational_decision_threshold: float = 0.40
    
    # Anomaly Detection Settings (Isolation Forest)
    anomaly_contamination: float = 0.05
    anomaly_n_estimators: int = 150
    
    # Supervised Failure Model Settings (XGBoost)
    xgb_max_depth: int = 4
    xgb_learning_rate: float = 0.05
    xgb_n_estimators: int = 200
    xgb_subsample: float = 0.8
    xgb_colsample_bytree: float = 0.8
    
    @classmethod
    def load_from_yaml(cls, yaml_path: Path = None) -> "MLConfig":
        instance = cls()
        if yaml_path is None:
            yaml_path = instance.config_dir / "risk_weights.yaml"
            
        if yaml_path.exists():
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data:
                    if "weights" in data:
                        instance.risk_weights = data["weights"]
                    if "thresholds" in data:
                        instance.risk_thresholds = data["thresholds"]
                    if "operational_decision_threshold" in data:
                        instance.operational_decision_threshold = float(data["operational_decision_threshold"])
        return instance

# Global default config instance
DEFAULT_CONFIG = MLConfig.load_from_yaml()
