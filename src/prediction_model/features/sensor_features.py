"""
Sensor degradation and dynamics feature engineering.
Implements rolling window statistics, physical stress indices, and degradation trends.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np

class SensorFeatureExtractor:
    def __init__(self, rated_temp_max: float = 95.0):
        self.rated_temp_max = rated_temp_max

    def extract_features_at_cutoff(
        self,
        asset_sensor_df: pd.DataFrame,
        cutoff_time: pd.Timestamp
    ) -> Dict[str, float]:
        """
        Extracts sensor degradation features strictly using observations <= cutoff_time.
        asset_sensor_df must contain sensor readings for a single asset.
        """
        # Strict point-in-time filter: no lookahead leakage
        history = asset_sensor_df[asset_sensor_df["timestamp"] <= cutoff_time].copy()
        if history.empty:
            return self._default_features()
            
        history.sort_values(by="timestamp", inplace=True)
        
        # Lookback windows
        history_24h = history[history["timestamp"] >= cutoff_time - pd.Timedelta(hours=24)]
        history_72h = history[history["timestamp"] >= cutoff_time - pd.Timedelta(hours=72)]
        history_7d = history[history["timestamp"] >= cutoff_time - pd.Timedelta(days=7)]
        
        # Fallbacks if window is empty
        h24 = history_24h if not history_24h.empty else history
        h72 = history_72h if not history_72h.empty else history
        h7d = history_7d if not history_7d.empty else history
        
        # Latest values
        latest = history.iloc[-1]
        
        # 1. Temperature metrics & headroom
        temp_mean_24h = float(h24["temperature_c"].mean())
        temp_max_24h = float(h24["temperature_c"].max())
        temp_std_24h = float(h24["temperature_c"].std(ddof=0))
        thermal_headroom = float(self.rated_temp_max - temp_max_24h)
        
        # Linear slope of temperature over 24h (°C / hour)
        if len(h24) >= 2:
            time_diffs_h = (h24["timestamp"] - h24["timestamp"].iloc[0]).dt.total_seconds() / 3600.0
            if time_diffs_h.max() > 0:
                slope, _ = np.polyfit(time_diffs_h, h24["temperature_c"], 1)
                temp_trend_24h = float(slope)
            else:
                temp_trend_24h = 0.0
        else:
            temp_trend_24h = 0.0
            
        # 2. Vibration metrics & RMS
        vib_mean_24h = float(h24["vibration_mms"].mean())
        vib_max_24h = float(h24["vibration_mms"].max())
        vib_rms_24h = float(np.sqrt(np.mean(h24["vibration_mms"]**2)))
        vib_crest_factor = float(vib_max_24h / (vib_mean_24h + 1e-6))
        
        # 3. Partial Discharge & Spikes
        pd_mean_24h = float(h24["partial_discharge_pc"].mean())
        pd_max_24h = float(h24["partial_discharge_pc"].max())
        # Spikes: count exceeding 80 pC or 3 sigma
        pd_spike_count_72h = int((h72["partial_discharge_pc"] > 75.0).sum())
        
        # 4. Oil Quality & Decay Rate (7-day degradation)
        oil_curr = float(latest["oil_quality_index"])
        oil_7d_ago = float(h7d.iloc[0]["oil_quality_index"])
        oil_decay_rate_7d = float(oil_7d_ago - oil_curr) # Positive if degrading
        
        # 5. Electrical Load Ratio & Voltage Deviation
        load_mean_24h = float(h24["load_current_a"].mean())
        volt_dev_std_24h = float(h24["voltage_deviation_pct"].std(ddof=0))
        
        return {
            "temp_mean_24h": temp_mean_24h,
            "temp_max_24h": temp_max_24h,
            "temp_std_24h": temp_std_24h,
            "thermal_headroom": thermal_headroom,
            "temp_trend_24h": temp_trend_24h,
            "vibration_mean_24h": vib_mean_24h,
            "vibration_max_24h": vib_max_24h,
            "vibration_rms_24h": vib_rms_24h,
            "vibration_crest_factor_24h": vib_crest_factor,
            "partial_discharge_mean_24h": pd_mean_24h,
            "partial_discharge_max_24h": pd_max_24h,
            "partial_discharge_spike_count_72h": float(pd_spike_count_72h),
            "oil_quality_current": oil_curr,
            "oil_quality_decay_rate_7d": oil_decay_rate_7d,
            "load_current_mean_24h": load_mean_24h,
            "voltage_deviation_std_24h": volt_dev_std_24h
        }

    def _default_features(self) -> Dict[str, float]:
        return {
            "temp_mean_24h": 50.0,
            "temp_max_24h": 55.0,
            "temp_std_24h": 2.0,
            "thermal_headroom": 40.0,
            "temp_trend_24h": 0.0,
            "vibration_mean_24h": 1.5,
            "vibration_max_24h": 2.0,
            "vibration_rms_24h": 1.5,
            "vibration_crest_factor_24h": 1.3,
            "partial_discharge_mean_24h": 20.0,
            "partial_discharge_max_24h": 30.0,
            "partial_discharge_spike_count_72h": 0.0,
            "oil_quality_current": 90.0,
            "oil_quality_decay_rate_7d": 0.0,
            "load_current_mean_24h": 200.0,
            "voltage_deviation_std_24h": 0.5
        }
