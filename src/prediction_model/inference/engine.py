"""
Unified inference engine for GridGuard AI ML subsystem.
Provides single-asset and batch scoring consumable by Django REST APIs and watsonx.ai.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd
import numpy as np

from registry.model_registry import ModelRegistry
from features.builder import FeatureBuilder
from scoring.risk_scorer import AssetRiskScorer
from explainability.explainer import PredictionExplainer
from config.settings import DEFAULT_CONFIG, MLConfig

class GridGuardInferenceEngine:
    def __init__(self, model_version: Optional[str] = None, config: Optional[MLConfig] = None):
        self.config = config or DEFAULT_CONFIG
        self.registry = ModelRegistry(self.config.artifacts_dir)
        self.failure_model, self.anomaly_detector, self.metadata = self.registry.load_bundle(model_version)
        
        self.feature_builder = FeatureBuilder(self.config)
        self.risk_scorer = AssetRiskScorer(self.config)
        self.explainer = PredictionExplainer(self.metadata.get("feature_importances", {}))
        self.operational_threshold = self.config.operational_decision_threshold

    def predict_asset(
        self,
        asset_id: str,
        assets_df: pd.DataFrame,
        sensors_df: pd.DataFrame,
        weather_df: pd.DataFrame,
        incidents_df: pd.DataFrame,
        maintenance_df: pd.DataFrame,
        cutoff_time: Optional[pd.Timestamp] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end inference pipeline for a single asset at cutoff_time.
        """
        if cutoff_time is None:
            cutoff_time = pd.to_datetime(sensors_df["timestamp"].max())
        else:
            cutoff_time = pd.to_datetime(cutoff_time)
            
        asset_matches = assets_df[assets_df["asset_id"] == asset_id]
        if asset_matches.empty:
            raise ValueError(f"Asset ID {asset_id} not found in asset repository.")
        asset_row = asset_matches.iloc[0]
        
        # 1. Build Features
        feat_dict = self.feature_builder.build_features_for_asset(
            asset_row, sensors_df, weather_df, incidents_df, maintenance_df, cutoff_time
        )
        feat_df = pd.DataFrame([feat_dict])
        
        # 2. Failure Probability
        p_failure = float(self.failure_model.predict_proba(feat_df)[0])
        failure_predicted = bool(p_failure >= self.operational_threshold)
        
        # 3. Anomaly Severity & Deviation
        asset_sensors = sensors_df[
            (sensors_df["asset_id"] == asset_id) & 
            (sensors_df["timestamp"] <= cutoff_time)
        ]
        if not asset_sensors.empty:
            latest_sensor = asset_sensors.sort_values(by="timestamp").iloc[-1].to_dict()
            s_anomaly = float(self.anomaly_detector.predict_anomaly_severity(pd.DataFrame([latest_sensor]))[0])
            is_anomaly = bool(s_anomaly >= 0.5)
            sensor_deviations = self.anomaly_detector.decompose_anomaly(latest_sensor)
        else:
            s_anomaly = 0.0
            is_anomaly = False
            sensor_deviations = []
            
        # 4. Multi-Factor Risk Scoring (SRS FR-10)
        risk_result = self.risk_scorer.compute_risk(
            failure_probability=p_failure,
            anomaly_severity=s_anomaly,
            weather_risk=feat_dict.get("composite_weather_risk", 0.0),
            historical_risk=feat_dict.get("historical_risk_index", 0.0),
            asset_criticality=feat_dict.get("criticality_normalized", 0.5)
        )
        
        # 5. Explainability & watsonx Grounding
        explanation = self.explainer.explain_prediction(
            asset_info=asset_row.to_dict(),
            features=feat_dict,
            risk_result=risk_result,
            sensor_deviations=sensor_deviations
        )
        
        # 6. Format Final Response Contract
        return {
            "asset_id": str(asset_id),
            "timestamp": cutoff_time.isoformat(),
            "model_version": self.metadata.get("model_version", "unknown"),
            "prediction_horizon_hours": self.config.prediction_horizon_hours,
            "lead_time_hours": self.config.lead_time_hours,
            "failure_probability": round(p_failure, 4),
            "failure_predicted": failure_predicted,
            "decision_threshold": self.operational_threshold,
            "sensor_anomaly": {
                "anomaly_score": round(s_anomaly, 4),
                "is_anomaly": is_anomaly,
                "abnormal_sensors": sensor_deviations
            },
            "risk_assessment": {
                "composite_risk_score": risk_result["composite_risk_score"],
                "risk_level": risk_result["risk_level"],
                "contributing_factors": risk_result["contributing_factors"]
            },
            "explainability": {
                "top_risk_drivers": explanation["top_risk_drivers"],
                "recommended_action": explanation["recommended_action"],
                "grounding_context_for_watsonx": explanation["grounding_context_for_watsonx"]
            }
        }

    def predict_batch(
        self,
        assets_df: pd.DataFrame,
        sensors_df: pd.DataFrame,
        weather_df: pd.DataFrame,
        incidents_df: pd.DataFrame,
        maintenance_df: pd.DataFrame,
        cutoff_time: Optional[pd.Timestamp] = None
    ) -> List[Dict[str, Any]]:
        """
        Runs predictions for all active assets and returns them sorted by risk descending (SRS FR-12).
        """
        results = []
        for a_id in assets_df["asset_id"]:
            res = self.predict_asset(
                a_id, assets_df, sensors_df, weather_df, incidents_df, maintenance_df, cutoff_time
            )
            results.append(res)
            
        results.sort(key=lambda x: x["risk_assessment"]["composite_risk_score"], reverse=True)
        return results
