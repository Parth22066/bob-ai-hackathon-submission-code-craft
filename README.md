# ⚡ GridGuard AI

> ### AI-Powered Predictive Maintenance & Power Outage Risk Advisor

GridGuard AI is an intelligent grid monitoring and decision-support platform designed to help power-grid operators predict equipment failures, identify high-risk assets, assess potential outage impact, and take preventive maintenance actions before failures occur.

The platform combines equipment telemetry, asset health information, weather conditions, historical maintenance/incidents, and machine-learning-based risk analysis to provide an actionable view of grid reliability.

---

## 👥 Team

| Field | Details |
|---|---|
| **Team Name** | CodeCraft |
| **Track** | AI |
| **Project** | GridGuard AI |
| **Problem Statement** | U1 — Power Outage Prediction & Grid Equipment Failure Advisor |
| **Team Lead** | Parth Yadav |
| **Team Members** | Mahi Vachhani, Unnati Solanki, Manav Rabadiya |

---

# 🎯 Problem Statement

Power-grid operators manage a large number of critical assets such as transformers, substations, and other electrical equipment. Equipment failures can occur due to abnormal operating conditions, environmental factors, aging, or inadequate maintenance.

Traditional maintenance approaches can make it difficult to identify which assets require immediate attention and which areas are most likely to experience outages.

**GridGuard AI addresses this challenge by combining equipment telemetry, asset health, weather conditions, and historical information to predict equipment failure risk and prioritize preventive actions.**

---

# 💡 Our Solution

GridGuard AI is an AI-powered decision-support system that evaluates the current and historical condition of grid assets and produces an understandable risk assessment.

The system:

1. Collects asset telemetry and operational data.
2. Processes sensor and environmental information.
3. Uses machine-learning models to identify abnormal conditions and estimate failure risk.
4. Combines asset risk with potential grid impact.
5. Prioritizes assets that require attention.
6. Provides maintenance recommendations.
7. Uses IBM watsonx.ai to generate human-readable explanations and assist operators in understanding the predictions.

The goal is to move from **reactive maintenance** toward **predictive and risk-based maintenance**.

---

# 🧠 How GridGuard AI Works

```text
┌──────────────────────────────┐
│        Data Sources          │
│                              │
│ • Asset Telemetry            │
│ • Equipment Health           │
│ • Weather Data               │
│ • Maintenance History        │
│ • Incident History           │
│ • Asset Information          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Data Processing &            │
│ Feature Engineering          │
│                              │
│ • Data Cleaning              │
│ • Normalization              │
│ • Feature Generation         │
│ • Anomaly Identification     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      AI / ML Engine          │
│                              │
│ • Failure Prediction         │
│ • Risk Prediction            │
│ • Anomaly Detection          │
│ • Asset Health Analysis      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│    Grid Impact Analysis      │
│                              │
│ • Potential Outage Impact    │
│ • Asset Criticality          │
│ • Area Risk                  │
│ • Priority Assessment        │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Decision & Recommendation    │
│ Engine                       │
│                              │
│ • Maintenance Priority       │
│ • Risk Ranking               │
│ • Crew Pre-positioning       │
│ • Preventive Actions         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      IBM watsonx.ai          │
│                              │
│ • AI Explanation             │
│ • Operator Assistance        │
│ • Natural Language Insights  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      GridGuard Dashboard     │
│                              │
│ • Risk Overview              │
│ • Asset Ranking              │
│ • Predictions                │
│ • Recommendations            │
│ • AI Insights                │
└──────────────────────────────┘
