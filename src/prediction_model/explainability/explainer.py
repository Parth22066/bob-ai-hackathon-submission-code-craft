"""
Model explainability and IBM watsonx.ai prompt grounding generator.
Implements SRS FR-17 and Section 6.
"""

from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd

class PredictionExplainer:
    def __init__(self, feature_importances: Dict[str, float]):
        self.feature_importances = feature_importances

    def explain_prediction(
        self,
        asset_info: Dict[str, Any],
        features: Dict[str, Any],
        risk_result: Dict[str, Any],
        sensor_deviations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Synthesizes top contributing factors and generates grounded watsonx context.
        """
        # 1. Identify Top Risk Drivers from Feature Importance and Elevation
        top_drivers = []
        for feat, imp in list(self.feature_importances.items())[:10]:
            val = features.get(feat, None)
            if val is not None and isinstance(val, (int, float)):
                # Determine risk direction
                direction = "elevating_risk"
                if "headroom" in feat and val > 25.0:
                    direction = "mitigating_risk"
                elif "oil_quality_current" in feat and val > 80.0:
                    direction = "mitigating_risk"
                    
                top_drivers.append({
                    "feature": feat,
                    "importance_weight": round(float(imp), 4),
                    "current_value": round(float(val), 2),
                    "direction": direction
                })
                
        # Pick top 4 drivers
        top_drivers = top_drivers[:4]
        
        # 2. Extract Abnormal Sensors
        abnormal_sensors = [d for d in sensor_deviations if d.get("is_abnormal", False)]
        
        # 3. Formulate Actionable Recommendations (FR-19)
        risk_level = risk_result["risk_level"]
        score = risk_result["composite_risk_score"]
        p_fail = risk_result["raw_inputs"]["failure_probability"]
        
        if risk_level == "Critical":
            rec_action = (
                "EMERGENCY ACTION: Pre-position emergency repair crew immediately. "
                "Initiate load shedding or circuit rerouting to relieve electrical stress. "
                "Conduct urgent physical inspection for active dielectric/thermal breakdown."
            )
        elif risk_level == "High":
            rec_action = (
                "PRIORITY MAINTENANCE: Dispatch maintenance crew within 24-48 hours. "
                "Perform thermographic scan, oil dissolved gas analysis (DGA), and vibration checks."
            )
        elif risk_level == "Medium":
            rec_action = (
                "ADVISORY MONITORING: Increase sensor sampling frequency. "
                "Schedule condition-based inspection during next standard maintenance window."
            )
        else:
            rec_action = "NORMAL OPERATIONS: Asset operating within standard nominal parameters."
            
        # 4. Construct Grounded watsonx.ai Context (FR-17, FR-18)
        watsonx_context = {
            "asset_id": asset_info.get("asset_id", "UNKNOWN"),
            "asset_name": asset_info.get("asset_name", "Transformer/Breaker"),
            "substation_id": asset_info.get("substation_id", "SUB-01"),
            "criticality_tier": asset_info.get("criticality_tier", 2),
            "current_risk_level": risk_level,
            "composite_risk_score": score,
            "failure_probability_pct": round(p_fail * 100.0, 1),
            "sensor_anomalies_detected": [
                f"{s['sensor']}: {s['value']} (Baseline mean: {s['baseline_mean']}, z-score: {s['z_score']})"
                for s in abnormal_sensors
            ],
            "environmental_conditions": {
                "composite_weather_risk": round(features.get("composite_weather_risk", 0.0), 2),
                "ambient_temp_max_24h": round(features.get("amb_temp_max_24h", 25.0), 1),
                "storm_warning_level": int(features.get("storm_level_max_24h", 0))
            },
            "operational_recommendation": rec_action
        }
        
        return {
            "top_risk_drivers": top_drivers,
            "abnormal_sensors": abnormal_sensors,
            "recommended_action": rec_action,
            "grounding_context_for_watsonx": watsonx_context
        }
