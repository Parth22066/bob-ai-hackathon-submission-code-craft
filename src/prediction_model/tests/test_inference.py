"""
Integration test for the unified inference engine and Django/watsonx output contracts.
"""

import pytest
import pandas as pd
from data.loader import DataLoader
from features.builder import FeatureBuilder, NUMERICAL_FEATURE_NAMES, CATEGORICAL_FEATURE_NAMES
from models.anomaly.isolation_forest import SensorAnomalyDetector
from models.failure.classifier import EquipmentFailureClassifier
from models.failure.calibrator import CalibratedFailureModel
from registry.model_registry import ModelRegistry
from inference.engine import GridGuardInferenceEngine
from inference.schemas import AssetPredictionOutput

def test_inference_engine_contract(tmp_path):
    loader = DataLoader()
    data = loader.load_all()
    
    # 1. Fit fast anomaly detector
    ad = SensorAnomalyDetector(n_estimators=30)
    ad.fit(data["sensors"].iloc[:200])
    
    # 2. Build minimal features & fit classifier
    fb = FeatureBuilder()
    df_feat = fb.build_training_dataset(
        data["assets"].iloc[:10], data["sensors"], data["weather"],
        data["incidents"], data["maintenance"],
        cutoff_interval_hours=72
    )
    
    X = df_feat[NUMERICAL_FEATURE_NAMES + CATEGORICAL_FEATURE_NAMES]
    y = df_feat["target_failure_next_H"]
    
    clf = EquipmentFailureClassifier(model_type="xgboost", n_estimators=20, max_depth=3)
    cal = CalibratedFailureModel(clf, method="sigmoid")
    cal.fit(X, y)
    
    # 3. Save to temporary registry
    reg = ModelRegistry(artifacts_dir=tmp_path)
    metadata = {
        "model_version": "test_v1",
        "feature_importances": clf.get_feature_importances(),
        "risk_weights": {"failure_probability": 0.35, "anomaly_severity": 0.20, "weather_risk": 0.15, "historical_incidents": 0.15, "asset_criticality": 0.15}
    }
    reg.save_bundle(cal, ad, metadata, "test_v1")
    
    # 4. Run inference engine
    from config.settings import MLConfig
    cfg = MLConfig(artifacts_dir=tmp_path)
    engine = GridGuardInferenceEngine(model_version="test_v1", config=cfg)
    
    target_asset = data["assets"]["asset_id"].iloc[0]
    pred = engine.predict_asset(
        target_asset, data["assets"], data["sensors"], data["weather"],
        data["incidents"], data["maintenance"]
    )
    
    # 5. Validate against Pydantic schema contract (strict enforcement)
    validated = AssetPredictionOutput(**pred)
    assert validated.asset_id == target_asset
    assert 0.0 <= validated.failure_probability <= 1.0
    assert 0.0 <= validated.risk_assessment.composite_risk_score <= 100.0
    assert validated.risk_assessment.risk_level in ["Low", "Medium", "High", "Critical"]
    assert len(validated.explainability.grounding_context_for_watsonx.operational_recommendation) > 0
