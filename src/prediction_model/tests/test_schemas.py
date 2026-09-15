"""
Unit tests for data validation and schema contracts.
"""

import pytest
import pandas as pd
from data.schemas import validate_dataframe, ASSET_COLUMNS, SENSOR_COLUMNS

def test_valid_asset_schema():
    df = pd.DataFrame([{
        "asset_id": "EQ-001",
        "asset_name": "Transformer 1",
        "asset_type": "Power Transformer",
        "substation_id": "SUB-01",
        "installation_date": "2020-01-01",
        "voltage_kv": 400.0,
        "rated_capacity_mva": 100.0,
        "criticality_tier": 3,
        "latitude": 28.5,
        "longitude": 77.2,
        "status": "active"
    }])
    valid, errors = validate_dataframe(df, ASSET_COLUMNS, "Assets")
    assert valid is True
    assert len(errors) == 0

def test_asset_schema_missing_column():
    df = pd.DataFrame([{
        "asset_id": "EQ-001",
        "asset_name": "Transformer 1"
    }])
    valid, errors = validate_dataframe(df, ASSET_COLUMNS, "Assets")
    assert valid is False
    assert any("Missing required column" in e for e in errors)

def test_sensor_bounds_validation():
    df = pd.DataFrame([{
        "reading_id": "R-1",
        "asset_id": "EQ-001",
        "timestamp": "2026-09-01 12:00:00",
        "temperature_c": 350.0, # Beyond max 160C
        "vibration_mms": 1.5,
        "partial_discharge_pc": 20.0,
        "oil_quality_index": 85.0,
        "load_current_a": 200.0,
        "voltage_deviation_pct": 1.2
    }])
    valid, errors = validate_dataframe(df, SENSOR_COLUMNS, "Sensors")
    assert valid is False
    assert any("outside [-40.0, 160.0]" in e for e in errors)
