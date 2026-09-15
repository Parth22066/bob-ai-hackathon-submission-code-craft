"""
Tests for anomaly detection, failure prediction, and probability calibration.
"""

import pytest
import numpy as np
import pandas as pd
from models.anomaly.isolation_forest import SensorAnomalyDetector
from models.failure.classifier import EquipmentFailureClassifier
from models.failure.calibrator import CalibratedFailureModel
from features.builder import NUMERICAL_FEATURE_NAMES, CATEGORICAL_FEATURE_NAMES

def test_anomaly_detector():
    df = pd.DataFrame({
        "temperature_c": np.random.normal(50, 5, 100),
        "vibration_mms": np.random.normal(1.5, 0.2, 100),
        "partial_discharge_pc": np.random.normal(25, 4, 100),
        "oil_quality_index": np.random.normal(90, 3, 100),
        "load_current_a": np.random.normal(200, 20, 100),
        "voltage_deviation_pct": np.random.normal(0, 0.5, 100)
    })
    detector = SensorAnomalyDetector(contamination=0.05, n_estimators=50)
    detector.fit(df)
    
    severities = detector.predict_anomaly_severity(df)
    assert len(severities) == 100
    assert np.all((severities >= 0.0) & (severities <= 1.0))
    
    # Check extreme anomaly decomposition
    extreme = {
        "temperature_c": 115.0,
        "vibration_mms": 12.0,
        "partial_discharge_pc": 400.0,
        "oil_quality_index": 30.0,
        "load_current_a": 500.0,
        "voltage_deviation_pct": 8.0
    }
    decomp = detector.decompose_anomaly(extreme)
    assert len(decomp) > 0
    assert any(d["is_abnormal"] for d in decomp)

def test_failure_classifier_and_calibration():
    np.random.seed(42)
    n = 150
    data = {}
    for feat in NUMERICAL_FEATURE_NAMES:
        data[feat] = np.random.normal(50, 10, n)
    for feat in CATEGORICAL_FEATURE_NAMES:
        data[feat] = np.random.choice(["Power Transformer", "Distribution Transformer"], n)
        
    df_X = pd.DataFrame(data)
    # Synthetic imbalanced target (10% positive)
    y = pd.Series((df_X["temp_max_24h"] > 60).astype(int))
    
    clf = EquipmentFailureClassifier(model_type="xgboost", n_estimators=30, max_depth=3)
    calibrated = CalibratedFailureModel(base_classifier=clf, method="sigmoid")
    calibrated.fit(df_X, y)
    
    probas = calibrated.predict_proba(df_X)
    assert len(probas) == n
    assert np.all((probas >= 0.0) & (probas <= 1.0))
    
    preds = calibrated.predict(df_X, threshold=0.40)
    assert len(preds) == n
    assert set(preds).issubset({0, 1})
