# GridGuard AI — Screenshots & Visual Artifacts

This folder houses visual artifacts, machine learning analysis plots, and application screenshots representing the GridGuard AI system.

## 1. Machine Learning Diagnostic Visualizations
- **`correlation_matrix.png`**: Pearson & Spearman correlation heatmaps detailing interdependencies between multi-modal sensor telemetry (temperature, vibration RMS, partial discharge, oil decay) and target failure probabilities.
- **`sensor_distributions_by_target.png`**: Empirical probability density distributions comparing healthy baseline operating states against anomalous pre-failure signatures.
- **`temporal_degradation_profile.png`**: Multi-week time-series tracking equipment degradation trajectory leading up to calibrated failure events.
- **`weather_and_storm_impact.png`**: Environmental strain analysis showing the correlation between wind gusts, precipitation, ambient heat, and accelerated transformer risk.

## 2. Key Web Application Views
- **Operator Dashboard (`/`)**: High-level grid KPI summary, active monitored transformers, critical failure alerts, and customer vulnerability counts.
- **Geospatial Risk Map (`/` section)**: Interactive map showing substation distribution and live risk heatmaps.
- **Risk Analysis Pipeline (`/risk`)**: Step-by-step decision flow tracing telemetry -> anomaly detection -> calibrated failure probability -> composite risk score -> maintenance recommendation.
- **watsonx.ai Copilot (`/ai`)**: Natural language operational assistant grounded in real-time telemetry context.
- **Consumer Transparency Portal (`/user`)**: Citizen-facing hub providing personalized connection health, proactive outage warnings, and one-click issue ticketing.
