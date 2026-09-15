"""
Multi-factor asset risk scoring engine.
Implements SRS FR-10 and Section 6.
Formula: Risk Score = 100 * (w_f*P_fail + w_a*S_anom + w_w*R_weather + w_h*R_hist + w_c*C_crit)
"""

from typing import Dict, Any, Optional
from config.settings import DEFAULT_CONFIG, MLConfig

class AssetRiskScorer:
    def __init__(self, config: Optional[MLConfig] = None):
        self.config = config or DEFAULT_CONFIG
        self.weights = self.config.risk_weights
        self.thresholds = self.config.risk_thresholds

    def compute_risk(
        self,
        failure_probability: float,
        anomaly_severity: float,
        weather_risk: float,
        historical_risk: float,
        asset_criticality: float # [0.25, 1.0]
    ) -> Dict[str, Any]:
        """
        Calculates composite asset risk score and risk level.
        All input factors are normalized in [0.0, 1.0].
        """
        # Clamp inputs
        p_fail = min(1.0, max(0.0, float(failure_probability)))
        s_anom = min(1.0, max(0.0, float(anomaly_severity)))
        r_weath = min(1.0, max(0.0, float(weather_risk)))
        r_hist = min(1.0, max(0.0, float(historical_risk)))
        c_crit = min(1.0, max(0.0, float(asset_criticality)))
        
        w_f = self.weights.get("failure_probability", 0.35)
        w_a = self.weights.get("anomaly_severity", 0.20)
        w_w = self.weights.get("weather_risk", 0.15)
        w_h = self.weights.get("historical_incidents", 0.15)
        w_c = self.weights.get("asset_criticality", 0.15)
        
        # Factor contributions (out of 100)
        comp_failure = round(100.0 * w_f * p_fail, 2)
        comp_anomaly = round(100.0 * w_a * s_anom, 2)
        comp_weather = round(100.0 * w_w * r_weath, 2)
        comp_history = round(100.0 * w_h * r_hist, 2)
        comp_criticality = round(100.0 * w_c * c_crit, 2)
        
        raw_score = comp_failure + comp_anomaly + comp_weather + comp_history + comp_criticality
        composite_score = round(min(100.0, max(0.0, raw_score)), 1)
        
        # Determine Risk Level (SRS Section 4.1)
        if composite_score >= self.thresholds.get("high", 85.0):
            risk_level = "Critical"
        elif composite_score >= self.thresholds.get("medium", 65.0):
            risk_level = "High"
        elif composite_score >= self.thresholds.get("low", 35.0):
            risk_level = "Medium"
        else:
            risk_level = "Low"
            
        return {
            "composite_risk_score": composite_score,
            "risk_level": risk_level,
            "contributing_factors": {
                "failure_probability_component": comp_failure,
                "sensor_anomaly_component": comp_anomaly,
                "weather_risk_component": comp_weather,
                "historical_incident_component": comp_history,
                "asset_criticality_component": comp_criticality
            },
            "raw_inputs": {
                "failure_probability": round(p_fail, 4),
                "anomaly_severity": round(s_anom, 4),
                "weather_risk": round(r_weath, 4),
                "historical_risk": round(r_hist, 4),
                "asset_criticality": round(c_crit, 4)
            }
        }
