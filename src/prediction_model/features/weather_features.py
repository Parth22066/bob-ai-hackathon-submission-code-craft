"""
Weather exposure and environmental feature engineering.
Computes rolling weather metrics, storm indices, and composite weather risk.
"""

from typing import Dict
import pandas as pd
import numpy as np

class WeatherFeatureExtractor:
    def extract_features_at_cutoff(
        self,
        substation_weather_df: pd.DataFrame,
        cutoff_time: pd.Timestamp
    ) -> Dict[str, float]:
        """
        Extracts environmental exposure features strictly using weather records <= cutoff_time.
        """
        history = substation_weather_df[substation_weather_df["timestamp"] <= cutoff_time].copy()
        if history.empty:
            return self._default_features()
            
        history_24h = history[history["timestamp"] >= cutoff_time - pd.Timedelta(hours=24)]
        h24 = history_24h if not history_24h.empty else history
        
        amb_temp_max_24h = float(h24["ambient_temperature_c"].max())
        amb_temp_mean_24h = float(h24["ambient_temperature_c"].mean())
        rain_total_24h = float(h24["rainfall_mm"].sum())
        wind_speed_max_24h = float(h24["wind_speed_kmh"].max())
        wind_gust_max_24h = float(h24["wind_gust_kmh"].max())
        lightning_count_24h = float(h24["lightning_strike_count"].sum())
        storm_level_max_24h = float(h24["storm_warning_level"].max())
        
        # Heat wave flag (operating under intense ambient heat)
        heat_wave_flag = 1.0 if amb_temp_max_24h > 38.0 else 0.0
        
        # Composite weather risk score [0, 1]
        # Combines normalized wind gust (0-120 km/h), rain (0-100 mm), storm warning (0-3), and lightning
        w_wind = min(1.0, max(0.0, (wind_gust_max_24h - 30.0) / 70.0))
        w_rain = min(1.0, max(0.0, rain_total_24h / 100.0))
        w_storm = storm_level_max_24h / 3.0
        w_lightning = min(1.0, lightning_count_24h / 25.0)
        
        composite_weather_risk = float(
            0.35 * w_wind + 0.25 * w_rain + 0.25 * w_storm + 0.15 * w_lightning
        )
        composite_weather_risk = min(1.0, max(0.0, composite_weather_risk))
        
        return {
            "amb_temp_max_24h": amb_temp_max_24h,
            "amb_temp_mean_24h": amb_temp_mean_24h,
            "rain_total_24h": rain_total_24h,
            "wind_speed_max_24h": wind_speed_max_24h,
            "wind_gust_max_24h": wind_gust_max_24h,
            "lightning_count_24h": lightning_count_24h,
            "storm_level_max_24h": storm_level_max_24h,
            "heat_wave_flag": heat_wave_flag,
            "composite_weather_risk": composite_weather_risk
        }

    def _default_features(self) -> Dict[str, float]:
        return {
            "amb_temp_max_24h": 30.0,
            "amb_temp_mean_24h": 28.0,
            "rain_total_24h": 0.0,
            "wind_speed_max_24h": 15.0,
            "wind_gust_max_24h": 20.0,
            "lightning_count_24h": 0.0,
            "storm_level_max_24h": 0.0,
            "heat_wave_flag": 0.0,
            "composite_weather_risk": 0.0
        }
