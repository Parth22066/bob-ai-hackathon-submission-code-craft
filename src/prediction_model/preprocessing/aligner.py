"""
Multi-source temporal alignment and resampling engine.
Implements SRS FR-06 (Timestamp Alignment).
"""

from typing import Dict, Optional
import pandas as pd
import numpy as np

class TemporalAligner:
    def __init__(self, freq: str = "3h"):
        self.freq = freq

    def align_and_merge(
        self,
        assets_df: pd.DataFrame,
        sensors_df: pd.DataFrame,
        weather_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Merges asset metadata, sensor telemetry, and local substation weather.
        Aligns on asset_id, substation_id, and timestamp.
        """
        # Ensure timestamps are datetimes
        sensors = sensors_df.copy()
        sensors["timestamp"] = pd.to_datetime(sensors["timestamp"])
        
        weather = weather_df.copy()
        weather["timestamp"] = pd.to_datetime(weather["timestamp"])
        
        # Merge asset metadata (substation_id, rated_capacity_mva, voltage_kv, criticality_tier)
        asset_meta = assets_df[["asset_id", "substation_id", "asset_type", "voltage_kv", "rated_capacity_mva", "criticality_tier", "installation_date"]].copy()
        merged = pd.merge(sensors, asset_meta, on="asset_id", how="inner")
        
        # Round timestamp to hourly or regular frequency for robust weather matching
        merged["weather_match_time"] = merged["timestamp"].dt.floor("h")
        weather["weather_match_time"] = weather["timestamp"].dt.floor("h")
        
        weather_cols = [
            "substation_id", "weather_match_time",
            "ambient_temperature_c", "rainfall_mm", "wind_speed_kmh",
            "wind_gust_kmh", "humidity_pct", "lightning_strike_count", "storm_warning_level"
        ]
        weather_dedup = weather[weather_cols].drop_duplicates(subset=["substation_id", "weather_match_time"])
        
        aligned = pd.merge(
            merged,
            weather_dedup,
            on=["substation_id", "weather_match_time"],
            how="left"
        )
        aligned.drop(columns=["weather_match_time"], inplace=True)
        aligned.sort_values(by=["asset_id", "timestamp"], inplace=True)
        aligned.reset_index(drop=True, inplace=True)
        return aligned
