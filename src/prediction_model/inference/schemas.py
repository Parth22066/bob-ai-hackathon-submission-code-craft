"""
Output schema specifications consumable by Django and IBM watsonx.ai.
Conforms strictly to Section 8 of the implementation plan.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class SensorDeviation(BaseModel):
    sensor: str
    value: float
    baseline_mean: float
    z_score: float
    is_abnormal: bool

class SensorAnomalyOutput(BaseModel):
    anomaly_score: float
    is_anomaly: bool
    abnormal_sensors: List[SensorDeviation]

class ContributingFactors(BaseModel):
    failure_probability_component: float
    sensor_anomaly_component: float
    weather_risk_component: float
    historical_incident_component: float
    asset_criticality_component: float

class RiskAssessmentOutput(BaseModel):
    composite_risk_score: float
    risk_level: str
    contributing_factors: ContributingFactors

class RiskDriver(BaseModel):
    feature: str
    importance_weight: float
    current_value: float
    direction: str

class WatsonxGroundingContext(BaseModel):
    asset_id: str
    asset_name: str
    substation_id: str
    criticality_tier: int
    current_risk_level: str
    composite_risk_score: float
    failure_probability_pct: float
    sensor_anomalies_detected: List[str]
    environmental_conditions: Dict[str, Any]
    operational_recommendation: str

class ExplainabilityOutput(BaseModel):
    top_risk_drivers: List[RiskDriver]
    recommended_action: str
    grounding_context_for_watsonx: WatsonxGroundingContext

class AssetPredictionOutput(BaseModel):
    asset_id: str
    timestamp: str
    model_version: str
    prediction_horizon_hours: int
    lead_time_hours: int
    failure_probability: float
    failure_predicted: bool
    decision_threshold: float
    sensor_anomaly: SensorAnomalyOutput
    risk_assessment: RiskAssessmentOutput
    explainability: ExplainabilityOutput
