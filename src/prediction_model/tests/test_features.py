"""
Tests for feature engineering and anti-leakage verification.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from features.sensor_features import SensorFeatureExtractor

def test_zero_lookahead_leakage():
    """
    CRITICAL TEST: Proves that future telemetry arriving after cutoff time t
    does NOT alter the features computed at cutoff time t.
    """
    extractor = SensorFeatureExtractor()
    cutoff = pd.Timestamp("2026-09-10 12:00:00")
    
    # Base history up to cutoff
    timestamps = pd.date_range(end=cutoff, periods=20, freq="h")
    df_base = pd.DataFrame({
        "timestamp": timestamps,
        "temperature_c": [50.0 + i * 0.2 for i in range(20)],
        "vibration_mms": [1.5 for _ in range(20)],
        "partial_discharge_pc": [25.0 for _ in range(20)],
        "oil_quality_index": [90.0 for _ in range(20)],
        "load_current_a": [300.0 for _ in range(20)],
        "voltage_deviation_pct": [0.0 for _ in range(20)]
    })
    
    feats_before = extractor.extract_features_at_cutoff(df_base, cutoff)
    
    # Append extreme future data occurring AFTER cutoff
    df_with_future = pd.concat([
        df_base,
        pd.DataFrame([{
            "timestamp": cutoff + pd.Timedelta(hours=1),
            "temperature_c": 140.0, # Extreme future spike
            "vibration_mms": 45.0,
            "partial_discharge_pc": 800.0,
            "oil_quality_index": 20.0,
            "load_current_a": 800.0,
            "voltage_deviation_pct": 15.0
        }])
    ], ignore_index=True)
    
    feats_after = extractor.extract_features_at_cutoff(df_with_future, cutoff)
    
    # Assert exact equality across all features
    for k in feats_before:
        assert feats_before[k] == feats_after[k], f"Leakage detected in feature {k}!"
