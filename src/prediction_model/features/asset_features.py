"""
Asset metadata, maintenance recency, and historical incident feature engineering.
"""

from typing import Dict, Any
import pandas as pd
import numpy as np

class AssetFeatureExtractor:
    def __init__(self, standard_maintenance_cycle_days: float = 90.0):
        self.standard_maintenance_cycle_days = standard_maintenance_cycle_days

    def extract_features_at_cutoff(
        self,
        asset_row: pd.Series,
        incidents_df: pd.DataFrame,
        maintenance_df: pd.DataFrame,
        cutoff_time: pd.Timestamp
    ) -> Dict[str, Any]:
        """
        Extracts asset lifecycle and historical reliability features strictly <= cutoff_time.
        """
        asset_id = asset_row["asset_id"]
        
        # 1. Age
        inst_date = pd.to_datetime(asset_row["installation_date"])
        age_years = max(0.1, (cutoff_time - inst_date).total_seconds() / (365.25 * 86400.0))
        
        # 2. Criticality & Electrical specs
        crit_tier = int(asset_row["criticality_tier"])
        crit_normalized = crit_tier / 4.0 # [0.25, 1.0]
        voltage_kv = float(asset_row["voltage_kv"])
        rated_mva = float(asset_row["rated_capacity_mva"])
        asset_type = str(asset_row["asset_type"])
        
        # 3. Incidents strictly in the past (<= cutoff_time)
        past_inc = incidents_df[
            (incidents_df["asset_id"] == asset_id) & 
            (incidents_df["start_timestamp"] <= cutoff_time)
        ]
        incident_count_lifetime = len(past_inc)
        
        past_90d_inc = past_inc[
            past_inc["start_timestamp"] >= cutoff_time - pd.Timedelta(days=90)
        ]
        incident_count_90d = len(past_90d_inc)
        
        if not past_inc.empty:
            last_inc_time = past_inc["start_timestamp"].max()
            days_since_last_failure = (cutoff_time - last_inc_time).total_seconds() / 86400.0
        else:
            days_since_last_failure = 365.0 * 5.0 # default: 5 years without failure
            
        # 4. Maintenance strictly in the past (<= cutoff_time)
        past_mnt = maintenance_df[
            (maintenance_df["asset_id"] == asset_id) & 
            (maintenance_df["completed_date"] <= cutoff_time) &
            (maintenance_df["status"] == "completed")
        ]
        
        if not past_mnt.empty:
            last_mnt_time = past_mnt["completed_date"].max()
            days_since_last_maintenance = max(0.0, (cutoff_time - last_mnt_time).total_seconds() / 86400.0)
        else:
            days_since_last_maintenance = 180.0
            
        overdue_maintenance_flag = 1.0 if days_since_last_maintenance > self.standard_maintenance_cycle_days else 0.0
        
        # Historical vulnerability index [0, 1]
        # Combines recent incidents and maintenance deficit
        h_inc = min(1.0, incident_count_90d / 2.0)
        h_overdue = min(1.0, max(0.0, (days_since_last_maintenance - self.standard_maintenance_cycle_days) / 60.0))
        historical_risk_index = min(1.0, max(0.0, 0.65 * h_inc + 0.35 * h_overdue))
        
        return {
            "asset_id": asset_id,
            "asset_type": asset_type,
            "age_years": float(age_years),
            "criticality_tier": crit_tier,
            "criticality_normalized": float(crit_normalized),
            "voltage_kv": voltage_kv,
            "rated_capacity_mva": rated_mva,
            "incident_count_lifetime": float(incident_count_lifetime),
            "incident_count_90d": float(incident_count_90d),
            "days_since_last_failure": float(days_since_last_failure),
            "days_since_last_maintenance": float(days_since_last_maintenance),
            "overdue_maintenance_flag": overdue_maintenance_flag,
            "historical_risk_index": float(historical_risk_index)
        }
