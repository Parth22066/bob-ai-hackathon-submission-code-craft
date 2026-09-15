"""
Data schema definitions and validation routines for GridGuard AI.
Adheres strictly to SRS Section 4.3, 7.1 and FR-02.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any
import pandas as pd
import numpy as np

# Canonical Schema Column Definitions
ASSET_COLUMNS = {
    "asset_id": "object",
    "asset_name": "object",
    "asset_type": "object",
    "substation_id": "object",
    "installation_date": "datetime64[ns]",
    "voltage_kv": "float64",
    "rated_capacity_mva": "float64",
    "criticality_tier": "int64",
    "latitude": "float64",
    "longitude": "float64",
    "status": "object",
}

SENSOR_COLUMNS = {
    "reading_id": "object",
    "asset_id": "object",
    "timestamp": "datetime64[ns]",
    "temperature_c": "float64",
    "vibration_mms": "float64",
    "partial_discharge_pc": "float64",
    "oil_quality_index": "float64",
    "load_current_a": "float64",
    "voltage_deviation_pct": "float64",
}

WEATHER_COLUMNS = {
    "weather_id": "object",
    "substation_id": "object",
    "timestamp": "datetime64[ns]",
    "ambient_temperature_c": "float64",
    "rainfall_mm": "float64",
    "wind_speed_kmh": "float64",
    "wind_gust_kmh": "float64",
    "humidity_pct": "float64",
    "lightning_strike_count": "int64",
    "storm_warning_level": "int64",
}

INCIDENT_COLUMNS = {
    "incident_id": "object",
    "asset_id": "object",
    "substation_id": "object",
    "start_timestamp": "datetime64[ns]",
    "end_timestamp": "datetime64[ns]",
    "incident_type": "object",
    "severity": "object",
    "duration_hours": "float64",
    "customers_affected": "int64",
}

MAINTENANCE_COLUMNS = {
    "maintenance_id": "object",
    "asset_id": "object",
    "scheduled_date": "datetime64[ns]",
    "completed_date": "datetime64[ns]",
    "maintenance_type": "object",
    "action_taken": "object",
    "parts_replaced": "object",
    "status": "object",
}

# Physical bounds for validation (FR-02)
VALUE_BOUNDS = {
    "temperature_c": (-40.0, 160.0),
    "vibration_mms": (0.0, 100.0),
    "partial_discharge_pc": (0.0, 5000.0),
    "oil_quality_index": (0.0, 100.0),
    "load_current_a": (0.0, 5000.0),
    "voltage_deviation_pct": (-50.0, 50.0),
    "ambient_temperature_c": (-50.0, 60.0),
    "rainfall_mm": (0.0, 500.0),
    "wind_speed_kmh": (0.0, 250.0),
    "wind_gust_kmh": (0.0, 350.0),
    "humidity_pct": (0.0, 100.0),
    "criticality_tier": (1, 4),
    "storm_warning_level": (0, 3),
}

def validate_dataframe(df: pd.DataFrame, expected_cols: Dict[str, str], name: str) -> Tuple[bool, List[str]]:
    """
    Validates a DataFrame against required columns and physical bounds.
    """
    errors = []
    if df is None or df.empty:
        return False, [f"DataFrame {name} is empty or None."]
        
    for col in expected_cols:
        if col not in df.columns:
            errors.append(f"{name}: Missing required column '{col}'")
            
    # Check value bounds
    for col, (min_v, max_v) in VALUE_BOUNDS.items():
        if col in df.columns:
            numeric_col = pd.to_numeric(df[col], errors="coerce")
            out_of_bounds = numeric_col[(numeric_col < min_v) | (numeric_col > max_v)]
            if len(out_of_bounds) > 0:
                errors.append(
                    f"{name}: Column '{col}' has {len(out_of_bounds)} values outside [{min_v}, {max_v}]. "
                    f"Min found: {numeric_col.min()}, Max found: {numeric_col.max()}"
                )
                
    return len(errors) == 0, errors
