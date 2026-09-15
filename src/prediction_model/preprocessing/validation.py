"""
GridGuard AI — Data Validation and Schema Integrity Engine.
Implements production-grade schema validation, data type enforcement,
duplicate detection, timestamp integrity, and missing-value analysis.
SRS FR-02 & Section 7.1.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
import numpy as np
import pandas as pd

GRIDGUARD_SCHEMA: Dict[str, Dict[str, Any]] = {
    "timestamp": {"dtype": "datetime64[ns]", "required": True, "type": "temporal"},
    "asset_id": {"dtype": "object", "required": True, "type": "categorical"},
    "asset_type": {"dtype": "object", "required": True, "type": "categorical"},
    "location": {"dtype": "object", "required": True, "type": "categorical"},
    "criticality": {"dtype": "int64", "required": True, "type": "ordinal", "min": 1, "max": 4},
    "age": {"dtype": "float64", "required": True, "type": "numeric", "min": 0.0, "max": 60.0},
    "capacity_load_importance": {"dtype": "float64", "required": True, "type": "numeric", "min": 1.0, "max": 500.0},
    "sensor_temperature": {"dtype": "float64", "required": True, "type": "numeric", "min": -40.0, "max": 160.0},
    "sensor_vibration": {"dtype": "float64", "required": True, "type": "numeric", "min": 0.0, "max": 100.0},
    "sensor_partial_discharge": {"dtype": "float64", "required": True, "type": "numeric", "min": 0.0, "max": 3000.0},
    "sensor_oil_quality": {"dtype": "float64", "required": True, "type": "numeric", "min": 0.0, "max": 100.0},
    "sensor_asset_health": {"dtype": "float64", "required": True, "type": "numeric", "min": 0.0, "max": 100.0},
    "weather_temperature": {"dtype": "float64", "required": True, "type": "numeric", "min": -50.0, "max": 60.0},
    "weather_rainfall": {"dtype": "float64", "required": True, "type": "numeric", "min": 0.0, "max": 500.0},
    "weather_wind_speed": {"dtype": "float64", "required": True, "type": "numeric", "min": 0.0, "max": 250.0},
    "weather_humidity": {"dtype": "float64", "required": True, "type": "numeric", "min": 0.0, "max": 100.0},
    "weather_storm_risk": {"dtype": "float64", "required": True, "type": "numeric", "min": 0.0, "max": 1.0},
    "historical_previous_failures": {"dtype": "int64", "required": True, "type": "numeric", "min": 0, "max": 50},
    "historical_outage_history": {"dtype": "float64", "required": True, "type": "numeric", "min": 0.0, "max": 1000.0},
    "historical_maintenance_count": {"dtype": "int64", "required": True, "type": "numeric", "min": 0, "max": 100},
    "historical_days_since_maintenance": {"dtype": "float64", "required": True, "type": "numeric", "min": 0.0, "max": 1500.0},
    "failure_within_horizon": {"dtype": "int64", "required": False, "type": "target", "min": 0, "max": 1}
}

@dataclass
class ValidationReport:
    is_valid: bool
    total_records: int
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    missing_analysis: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    duplicate_count: int = 0
    outlier_counts: Dict[str, int] = field(default_factory=dict)
    timestamp_summary: Dict[str, Any] = field(default_factory=dict)

class DataValidator:
    def __init__(self, schema: Optional[Dict[str, Dict[str, Any]]] = None):
        self.schema = schema or GRIDGUARD_SCHEMA

    def validate(self, df: pd.DataFrame, is_training: bool = True) -> Tuple[bool, ValidationReport]:
        errors: List[str] = []
        warnings: List[str] = []
        outlier_counts: Dict[str, int] = {}
        missing_analysis: Dict[str, Dict[str, Any]] = {}
        
        if df is None or df.empty:
            return False, ValidationReport(
                is_valid=False, total_records=0, errors=["DataFrame is empty or None."]
            )
            
        n_records = len(df)
        
        for col, meta in self.schema.items():
            if meta.get("required", False):
                if col not in df.columns:
                    errors.append(f"Missing required column: '{col}'")
            elif col == "failure_within_horizon" and is_training:
                if col not in df.columns:
                    errors.append(f"Training data requires target column '{col}'")
                    
        if "asset_id" in df.columns and "timestamp" in df.columns:
            dups = df.duplicated(subset=["asset_id", "timestamp"]).sum()
            duplicate_count = int(dups)
            if duplicate_count > 0:
                warnings.append(f"Detected {duplicate_count} duplicate (asset_id, timestamp) rows.")
        else:
            duplicate_count = 0

        ts_summary = {}
        if "timestamp" in df.columns:
            try:
                parsed_ts = pd.to_datetime(df["timestamp"], errors="coerce")
                null_ts = parsed_ts.isna().sum()
                if null_ts > 0:
                    errors.append(f"Timestamp column contains {null_ts} unparseable / null values.")
                else:
                    ts_summary = {
                        "min_timestamp": str(parsed_ts.min()),
                        "max_timestamp": str(parsed_ts.max()),
                        "total_time_span_days": round((parsed_ts.max() - parsed_ts.min()).total_seconds() / 86400.0, 2)
                    }
                    if "asset_id" in df.columns:
                        is_monotonic = df.groupby("asset_id")["timestamp"].apply(
                            lambda s: pd.to_datetime(s).is_monotonic_increasing
                        ).all()
                        if not is_monotonic:
                            warnings.append("Timestamps are not monotonically increasing per asset. Sorting required.")
            except Exception as e:
                errors.append(f"Timestamp validation failed with error: {str(e)}")

        for col in df.columns:
            n_missing = int(df[col].isna().sum())
            pct_missing = round(float(n_missing / n_records * 100.0), 2)
            missing_analysis[col] = {
                "missing_count": n_missing,
                "missing_pct": pct_missing
            }
            if pct_missing > 20.0:
                warnings.append(f"High missingness in '{col}': {pct_missing}% null.")
            elif pct_missing > 0.0 and col in ["asset_id", "timestamp"]:
                errors.append(f"Primary key '{col}' contains {n_missing} missing values.")

        for col, meta in self.schema.items():
            if col in df.columns and meta.get("type") in ["numeric", "ordinal"]:
                min_v = meta.get("min")
                max_v = meta.get("max")
                if min_v is not None and max_v is not None:
                    series = pd.to_numeric(df[col], errors="coerce").dropna()
                    violators = ((series < min_v) | (series > max_v)).sum()
                    if violators > 0:
                        outlier_counts[col] = int(violators)
                        warnings.append(
                            f"Column '{col}' has {violators} values outside physical bounds [{min_v}, {max_v}]."
                        )

        is_valid = len(errors) == 0
        report = ValidationReport(
            is_valid=is_valid,
            total_records=n_records,
            errors=errors,
            warnings=warnings,
            missing_analysis=missing_analysis,
            duplicate_count=duplicate_count,
            outlier_counts=outlier_counts,
            timestamp_summary=ts_summary
        )
        return is_valid, report

    def sanitize(self, df: pd.DataFrame, drop_duplicates: bool = True) -> pd.DataFrame:
        cleaned = df.copy()
        if "timestamp" in cleaned.columns:
            cleaned["timestamp"] = pd.to_datetime(cleaned["timestamp"])
        if drop_duplicates and "asset_id" in cleaned.columns and "timestamp" in cleaned.columns:
            cleaned = cleaned.drop_duplicates(subset=["asset_id", "timestamp"]).reset_index(drop=True)
        if "asset_id" in cleaned.columns and "timestamp" in cleaned.columns:
            cleaned = cleaned.sort_values(by=["asset_id", "timestamp"]).reset_index(drop=True)
        return cleaned
