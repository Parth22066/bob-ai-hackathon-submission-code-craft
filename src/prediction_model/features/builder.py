"""
Feature union and point-in-time training matrix builder.
Guarantees zero future lookahead leakage by strict cutoff slicing.
"""

from typing import Dict, List, Tuple, Optional, Any
import pandas as pd
import numpy as np

from features.sensor_features import SensorFeatureExtractor
from features.weather_features import WeatherFeatureExtractor
from features.asset_features import AssetFeatureExtractor
from config.settings import DEFAULT_CONFIG

NUMERICAL_FEATURE_NAMES = [
    "temp_mean_24h", "temp_max_24h", "temp_std_24h", "thermal_headroom", "temp_trend_24h",
    "vibration_mean_24h", "vibration_max_24h", "vibration_rms_24h", "vibration_crest_factor_24h",
    "partial_discharge_mean_24h", "partial_discharge_max_24h", "partial_discharge_spike_count_72h",
    "oil_quality_current", "oil_quality_decay_rate_7d", "load_current_mean_24h", "voltage_deviation_std_24h",
    "amb_temp_max_24h", "amb_temp_mean_24h", "rain_total_24h", "wind_speed_max_24h", "wind_gust_max_24h",
    "lightning_count_24h", "storm_level_max_24h", "heat_wave_flag", "composite_weather_risk",
    "age_years", "criticality_normalized", "voltage_kv", "rated_capacity_mva",
    "incident_count_lifetime", "incident_count_90d", "days_since_last_failure",
    "days_since_last_maintenance", "overdue_maintenance_flag", "historical_risk_index"
]

CATEGORICAL_FEATURE_NAMES = [
    "asset_type"
]

class FeatureBuilder:
    def __init__(self, config=None):
        self.config = config or DEFAULT_CONFIG
        self.sensor_extractor = SensorFeatureExtractor()
        self.weather_extractor = WeatherFeatureExtractor()
        self.asset_extractor = AssetFeatureExtractor()

    def build_features_for_asset(
        self,
        asset_row: pd.Series,
        sensor_df: pd.DataFrame,
        weather_df: pd.DataFrame,
        incidents_df: pd.DataFrame,
        maintenance_df: pd.DataFrame,
        cutoff_time: pd.Timestamp
    ) -> Dict[str, Any]:
        """
        Builds a single point-in-time feature dictionary for one asset at cutoff_time.
        Strictly observes timestamp <= cutoff_time.
        """
        asset_id = asset_row["asset_id"]
        sub_id = asset_row["substation_id"]
        
        # 1. Asset features
        asset_feats = self.asset_extractor.extract_features_at_cutoff(
            asset_row, incidents_df, maintenance_df, cutoff_time
        )
        
        # 2. Sensor features
        asset_sensors = sensor_df[sensor_df["asset_id"] == asset_id]
        sensor_feats = self.sensor_extractor.extract_features_at_cutoff(
            asset_sensors, cutoff_time
        )
        
        # 3. Weather features
        sub_weather = weather_df[weather_df["substation_id"] == sub_id]
        weather_feats = self.weather_extractor.extract_features_at_cutoff(
            sub_weather, cutoff_time
        )
        
        combined = {}
        combined.update(asset_feats)
        combined.update(sensor_feats)
        combined.update(weather_feats)
        combined["cutoff_timestamp"] = cutoff_time
        return combined

    def build_training_dataset(
        self,
        assets_df: pd.DataFrame,
        sensors_df: pd.DataFrame,
        weather_df: pd.DataFrame,
        incidents_df: pd.DataFrame,
        maintenance_df: pd.DataFrame,
        cutoff_interval_hours: int = 12
    ) -> pd.DataFrame:
        """
        Generates a leak-free point-in-time feature matrix across time cutoffs.
        Evaluates forward failure target within (cutoff + lead_time, cutoff + horizon].
        """
        H = pd.Timedelta(hours=self.config.prediction_horizon_hours)
        L = pd.Timedelta(hours=self.config.lead_time_hours)
        
        min_time = sensors_df["timestamp"].min() + pd.Timedelta(days=7) # Lookback warm-up
        max_time = sensors_df["timestamp"].max() - H # Avoid right-censoring
        
        if min_time >= max_time:
            raise ValueError("Insufficient time range for the specified horizon and warm-up window.")
            
        cutoffs = pd.date_range(start=min_time, end=max_time, freq=f"{cutoff_interval_hours}h")
        
        rows = []
        for cutoff in cutoffs:
            target_start = cutoff + L
            target_end = cutoff + H
            
            # Identify incidents occurring in the forward window
            forward_incidents = incidents_df[
                (incidents_df["start_timestamp"] > target_start) &
                (incidents_df["start_timestamp"] <= target_end)
            ]
            failing_asset_ids = set(forward_incidents["asset_id"].unique())
            
            for _, asset_row in assets_df.iterrows():
                a_id = asset_row["asset_id"]
                feat_dict = self.build_features_for_asset(
                    asset_row, sensors_df, weather_df, incidents_df, maintenance_df, cutoff
                )
                feat_dict["target_failure_next_H"] = 1 if a_id in failing_asset_ids else 0
                rows.append(feat_dict)
                
        df_dataset = pd.DataFrame(rows)
        return df_dataset
