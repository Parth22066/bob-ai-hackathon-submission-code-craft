import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
"""
Comprehensive Unit & Integration Tests for GridGuard AI Preprocessing Pipeline.
Tests validation, feature engineering, zero-leakage, outlier clipping,
imputation, pipeline serialization, and inference parity.
"""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from validation import DataValidator, GRIDGUARD_SCHEMA
from feature_engineering import TemporalFeatureEngineer
from preprocessing import GridGuardPreprocessingPipeline, DomainOutlierClipper

@pytest.fixture
def sample_raw_data():
    """Generates a small test slice matching the dataset schema."""
    timestamps = pd.date_range(start="2026-09-01", periods=15, freq="4h")
    data = []
    for a_id in ["EQ-001", "EQ-002"]:
        for i, ts in enumerate(timestamps):
            data.append({
                "timestamp": ts,
                "asset_id": a_id,
                "asset_type": "Power Transformer",
                "location": "Substation North",
                "criticality": 3,
                "age": 12.5,
                "capacity_load_importance": 80.0,
                "sensor_temperature": 50.0 + i * 0.5,
                "sensor_vibration": 1.8 + i * 0.05,
                "sensor_partial_discharge": 22.0 + i * 1.5,
                "sensor_oil_quality": 92.0 - i * 0.2,
                "sensor_asset_health": 95.0 - i * 0.8,
                "weather_temperature": 28.0,
                "weather_rainfall": 0.0,
                "weather_wind_speed": 15.0,
                "weather_humidity": 55.0,
                "weather_storm_risk": 0.1,
                "historical_previous_failures": 1,
                "historical_outage_history": 8.5,
                "historical_maintenance_count": 4,
                "historical_days_since_maintenance": 45.0 + i * 0.16,
                "failure_within_horizon": 0 if i < 12 else 1
            })
    return pd.DataFrame(data)

def test_validator_required_fields_and_schema(sample_raw_data):
    validator = DataValidator()
    is_valid, report = validator.validate(sample_raw_data)
    assert is_valid is True
    assert len(report.errors) == 0

    # Test missing required column
    corrupted = sample_raw_data.drop(columns=["sensor_temperature"])
    is_valid, report = validator.validate(corrupted)
    assert is_valid is False
    assert any("sensor_temperature" in e for e in report.errors)

def test_validator_duplicate_detection(sample_raw_data):
    validator = DataValidator()
    # Duplicate first row
    dup_df = pd.concat([sample_raw_data, sample_raw_data.iloc[[0]]], ignore_index=True)
    is_valid, report = validator.validate(dup_df)
    assert report.duplicate_count == 1
    
    # Sanitization deduplicates cleanly
    sanitized = validator.sanitize(dup_df)
    assert len(sanitized) == len(sample_raw_data)

def test_zero_lookahead_in_temporal_feature_engineer(sample_raw_data):
    """
    CRITICAL TEST: Ensures that adding future observations does NOT alter
    the rolling features computed at time cutoff t.
    """
    engineer = TemporalFeatureEngineer(sampling_interval_hours=4)
    engineer.fit(sample_raw_data)
    
    # Compute features on original data
    feats_orig = engineer.transform(sample_raw_data)
    target_row_idx = 10 # Observation at t=10
    orig_values = feats_orig.iloc[target_row_idx][["temp_mean_24h", "vibration_rms_24h", "pd_mean_24h"]].to_dict()
    
    # Append extreme future data occurring AFTER the slice
    future_time = pd.to_datetime(sample_raw_data["timestamp"].max()) + pd.Timedelta(hours=4)
    future_row = sample_raw_data.iloc[[-1]].copy()
    future_row["timestamp"] = future_time
    future_row["sensor_temperature"] = 155.0 # Extreme future spike
    future_row["sensor_vibration"] = 35.0
    future_row["sensor_partial_discharge"] = 900.0
    
    expanded_df = pd.concat([sample_raw_data, future_row], ignore_index=True)
    feats_expanded = engineer.transform(expanded_df)
    expanded_values = feats_expanded.iloc[target_row_idx][["temp_mean_24h", "vibration_rms_24h", "pd_mean_24h"]].to_dict()
    
    # Values at historical t=10 must be identical
    for k in orig_values:
        assert orig_values[k] == pytest.approx(expanded_values[k], rel=1e-5), f"Leakage detected in {k}!"

def test_missing_value_imputation_in_pipeline(sample_raw_data):
    # Introduce NaNs in sensors
    corrupted = sample_raw_data.copy()
    corrupted.loc[2:5, "sensor_temperature"] = np.nan
    corrupted.loc[6:8, "sensor_vibration"] = np.nan
    corrupted.loc[9:11, "sensor_oil_quality"] = np.nan
    
    pipeline = GridGuardPreprocessingPipeline()
    X_trans, df_trans = pipeline.fit_transform(corrupted)
    
    # Transformed data must have 0 NaNs
    assert np.isnan(X_trans).sum() == 0
    assert df_trans.isna().sum().sum() == 0

def test_outlier_clipping_learned_on_train(sample_raw_data):
    clipper = DomainOutlierClipper(lower_percentile=1.0, upper_percentile=99.0)
    clipper.fit(sample_raw_data)
    
    # Create test sample with extreme glitch
    extreme_test = sample_raw_data.copy()
    extreme_test.loc[0, "sensor_temperature"] = 250.0 # Far beyond normal
    
    clipped = clipper.transform(extreme_test)
    high_bound = clipper.bounds_["sensor_temperature"][1]
    assert clipped.loc[0, "sensor_temperature"] <= high_bound
    assert clipped.loc[0, "sensor_temperature"] < 250.0

def test_pipeline_serialization_and_inference_parity(sample_raw_data, tmp_path):
    pipeline = GridGuardPreprocessingPipeline(artifacts_dir=tmp_path)
    X_trans1, df_trans1 = pipeline.fit_transform(sample_raw_data)
    
    # Save to disk
    save_path = pipeline.save(tmp_path / "fitted_pipeline.joblib")
    assert save_path.exists()
    
    # Load and transform test slice
    loaded_pipeline = GridGuardPreprocessingPipeline.load(save_path)
    X_trans2, df_trans2 = loaded_pipeline.transform(sample_raw_data)
    
    # Outputs must be bit-for-bit identical
    np.testing.assert_allclose(X_trans1, X_trans2, rtol=1e-6)
    assert df_trans1.columns.tolist() == df_trans2.columns.tolist()
