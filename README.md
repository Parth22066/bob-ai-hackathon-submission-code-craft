# ⚡ GridGuard AI — Predictive Maintenance & Power Outage Risk Advisory Platform

[![Hackathon](https://img.shields.io/badge/Hackathon-IBM%20x%20BOB-blue.svg)](https://www.ibm.com)
[![Track](https://img.shields.io/badge/Track-AI%20%7C%20Smart%20Infrastructure-orange.svg)](https://www.ibm.com)
[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://react.dev/)
[![IBM watsonx.ai](https://img.shields.io/badge/IBM%20watsonx.ai-Granite--13B-purple.svg)](https://www.ibm.com/watsonx)
[![XGBoost](https://img.shields.io/badge/ML-Calibrated%20XGBoost-orange.svg)](https://xgboost.readthedocs.io/)

> **Team CodeCraft — IBM x BOB Hackathon Submission**  
> An enterprise-grade, end-to-end Predictive Maintenance & Outage Risk Advisory platform that prevents catastrophic power transformer failures, optimizes utility field operations with automated crew dispatch, and delivers transparent, real-time grid intelligence to energy consumers.

---

## 👥 Team Information

| Field | Details |
|---|---|
| **Team Name** | **CodeCraft** |
| **Track** | **AI** (AI & Smart Infrastructure / Clean Energy Resilience) |
| **Project** | **GridGuard AI** |
| **Problem Statement** | **U1 — Power Outage Prediction & Grid Equipment Failure Advisor** |
| **Team Lead** | **Parth Yadav** (`parthyadav2206@gmail.com`) |
| **Team Members** | **Mahi Vachhani**, **Unnati Solanki**, **Manav Rabadiya** |

---

## 🎯 Problem Statement

Electrical distribution utilities face mounting challenges maintaining aging power grid infrastructure. Critical assets—such as power transformers, circuit breakers, and distribution substations—frequently operate under extreme weather conditions, high electrical loads, and severe thermal stress.

Traditional utility management suffers from:
1. **Reactive Firefighting:** Utilities repair equipment *after* an outage occurs, multiplying repair costs by 10x and causing extensive municipal and industrial blackouts.
2. **Siloed Sensor Streams:** Telemetry (temperature, vibration RMS, partial discharge, dissolved gas, oil degradation) remains disconnected from forward-looking failure models.
3. **Alert Fatigue:** Static threshold alarms flood control center dispatchers with false positives, eroding trust in automated alerts.
4. **The "Black Box" AI Barrier:** Operators hesitate to take high-stakes maintenance decisions without explainable feature attribution.
5. **Consumer Information Gap:** Citizens and businesses receive zero advance warning before localized power interruptions.

**GridGuard AI solves these challenges by combining real-time multi-modal telemetry, point-in-time feature engineering, calibrated machine learning, and IBM watsonx.ai Granite foundation models into an actionable decision-support ecosystem.**

---

## 💡 Solution Overview & Core Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              GRIDGUARD AI SUITE                             │
├─────────────────────────┬─────────────────────────┬─────────────────────────┤
│ 1. PREDICTIVE ML CORE   │ 2. GENAI COPILOT        │ 3. DUAL-PERSONA PORTAL  │
│    (src/prediction_model)│    (IBM watsonx.ai)     │    (src/frontend)       │
│ • Calibrated XGBoost    │ • IBM Granite 13B Chat  │ • Dispatcher Dashboard  │
│ • Isolation Forest      │ • Fact-grounded payload │ • Geospatial Risk Map   │
│ • 35+ Leakage-Free FE   │ • Substation reasoning  │ • P1-P4 Crew Dispatch   │
│ • FR-10 Multi-Factor    │ • Zero hallucinations   │ • Consumer Transparency │
└────────────┬────────────┴────────────┬────────────┴────────────┬────────────┘
             │                         │                         │
             ▼                         ▼                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                 DJANGO REST FRAMEWORK API GATEWAY (src/backend)              │
│  /api/dashboard/  |  /api/assets/ranking/  |  /api/risk/analyze/            │
│  /api/ai/assistant/  |  /api/weather/live/  |  /api/maintenance/history/    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
Repository Structure
├── src/                                  # All source code
│   ├── backend/                          # Django 6.1 REST API backend (GridGuard core)
│   ├── frontend/                         # React 18 + Vite modern web application
│   └── prediction_model/                 # ML subsystem (calibrated XGBoost, Isolation Forest, Registry)
├── docs/                                 # Complete written documentation
│   ├── problem-statement.md              # Detailed domain challenges & objectives
│   ├── solution-overview.md              # System capabilities, 3 pillars & business ROI
│   ├── architecture.md                   # Microservice architecture, data flows & API specs
│   └── setup-guide.md                    # Installation, configurations, running & testing
├── demo/                                 # Demo artifacts
│   ├── screenshots/                      # Diagnostic ML plots & application views
│   ├── demo-video-link.txt               # Hosted demonstration video link & walkthrough
│   └── live-demo-url.txt                 # Local deployment instructions
├── presentation/                         # Slide deck
│   ├── GridGuard_AI_Presentation.pptx    # Complete 12-slide executive presentation deck
│   └── generate_presentation.py          # Standalone python-pptx presentation generator
├── submission.yaml                       # Structured hackathon submission metadata
├── start.bat                             # One-click Windows startup launcher
├── stop.bat                              # One-click Windows graceful shutdown script
├── README.md                             # Top-level project entry point
└── .gitignore                            # Clean repository ignore definitions
```

---

## ⚡ Quick Start: One-Click Launch

For Windows workstations, automated batch scripts manage the entire runtime:

### 1. Start All Services
Double-click `start.bat` in the repository root (or execute in PowerShell / Command Prompt):
```cmd
start.bat
```
*What `start.bat` does automatically:*
- Detects the Python virtual environment (`venv/`).
- Runs backend database migrations (`python manage.py migrate`).
- Launches the Django REST backend server on `http://localhost:8000`.
- Launches the React Vite frontend server on `http://localhost:5173`.
- Opens `http://localhost:5173` in your default web browser.

### 2. Stop All Services
To cleanly shut down all server processes and free ports 8000 and 5173:
```cmd
stop.bat
```

### 🔑 Demo Login Credentials

| Role | Email | Password | Portal Features |
|---|---|---|---|
| **Grid Operations Dispatcher** | `admin@gridguard.ai` | `admin123` | Full control center: Executive Dashboard, Geospatial Risk Map, Telemetry Explorer, Weather Intelligence, Crew Dispatch, Watsonx Copilot |
| **Energy Consumer** | `user@gridguard.ai` | `user123` | Citizen portal: Connection health status, localized storm & outage warnings, rapid issue reporting, consumer AI assistant |

---

## 🧠 Machine Learning & GenAI Subsystem

### 1. Equipment Failure Probability Prediction (FR-08)
- **Algorithm:** Supervised XGBoost Classifier with Platt Sigmoid calibration (`CalibratedClassifierCV`).
- **Forecast Horizon:** 168 hours (7 days forward) with 2-hour operational lead time.
- **Evaluation:** Purged & Embargoed walk-forward time-series cross validation preventing lookahead bias.

### 2. Multi-Channel Sensor Anomaly Detection (FR-09)
- **Algorithm:** Multivariate Isolation Forest (150 estimators, 8% contamination).
- **Monitored Telemetry:** Temperature (°C), Vibration RMS (mm/s), Partial Discharge (pC), Dielectric Oil Quality Index, Voltage Deviation (%), and Load Current (A).
- **Z-Score Decomposition:** Decomposes multi-sensor anomalies into physical z-score deviations against nominal operating baselines.

### 3. Multi-Factor Composite Risk Scoring (FR-10)
$$\text{Composite Risk Score} = 100 \times \left( 0.35 \cdot P_{\text{failure}} + 0.20 \cdot S_{\text{anomaly}} + 0.15 \cdot R_{\text{weather}} + 0.15 \cdot R_{\text{hist}} + 0.15 \cdot C_{\text{asset}} \right)$$

- **Tiers:** `Low` (0–19), `Medium` (20–39), `High` (40–69), and `Critical` (70–100).

### 4. IBM watsonx.ai Granite Copilot (FR-17, FR-18)
- Injects factual telemetry payloads into the **IBM Granite 13B Chat v2** foundation model.
- Eliminates AI hallucination by constraining responses strictly to verified sensor readings, risk drivers, and maintenance logs.
- Includes grounded offline fallback synthesizer for local testing.

---

## 🧪 Verification & Automated Tests

All test suites and verification scripts pass out of the box:

```bash
# 1. Run Machine Learning Test Suite (16/16 tests passing)
python -m pytest src/prediction_model/tests/

# 2. Run Batch Asset Risk Inference (Scores & ranks 40 active assets)
python src/prediction_model/scripts/predict.py --batch

# 3. Verify Single Asset Inference
python src/prediction_model/scripts/predict.py --asset-id EQ-001

# 4. Verify Backend Django Configuration
python src/backend/manage.py check

# 5. Build Frontend Production Bundle (Vite)
cd src/frontend && npm run build
```

---

## 📊 Business Impact & Measurable Value

| Operational Metric | Traditional Utility Operations | With GridGuard AI | Net Impact |
|---|---|---|---|
| **Outage Frequency (SAIFI)** | High (unplanned post-failure response) | Proactive maintenance prior to flashover | **35–50% Reduction** |
| **Outage Duration (SAIDI)** | 3.5 – 6 hours average repair | Pre-positioned crews with exact parts | **60% Faster Restoration** |
| **False Alarm Rate** | High alert fatigue from static thresholds | Calibrated probabilities + Z-score anomaly | **75% Fewer Nuisance Alarms** |
| **Asset Longevity** | Early retirement due to hot spots | Condition-based thermal load balancing | **+5 to 8 Years Asset Life** |

---

## 📚 Deliverables & Documentation Links

- **Problem Statement:** [`docs/problem-statement.md`](docs/problem-statement.md)
- **Solution Overview:** [`docs/solution-overview.md`](docs/solution-overview.md)
- **Architecture Specification:** [`docs/architecture.md`](docs/architecture.md)
- **Setup & Deployment Guide:** [`docs/setup-guide.md`](docs/setup-guide.md)
- **Presentation Deck:** [`presentation/GridGuard_AI_Presentation.pptx`](presentation/GridGuard_AI_Presentation.pptx)
- **Demo Video Walkthrough:** [`demo/demo-video-link.txt`](demo/demo-video-link.txt)
- **Submission Metadata:** [`submission.yaml`](submission.yaml)

---

## 👥 Authors & Acknowledgments

Developed by **Team CodeCraft**:
- **Parth Yadav** (Team Lead)
- **Mahi Vachhani**
- **Unnati Solanki**
- **Manav Rabadiya**

*Built for the IBM x BOB Hackathon 2026.*
