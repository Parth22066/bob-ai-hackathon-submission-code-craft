# Problem Statement: GridGuard AI

## 1. Domain Background & Operational Context
Electrical power distribution networks are the lifeblood of modern economic and urban infrastructure. Within these networks, power transformers, circuit breakers, and distribution substations operate continuously under harsh environmental conditions and variable consumer load profiles. In developing and rapidly expanding regions, utility infrastructure is burdened by:

- **Aging Capital Assets:** Many substation transformers operate past their nominal design life (25–35+ years), with deteriorating winding insulation, dielectric oil breakdown, and high mechanical stress.
- **Extreme Weather Exposure:** Unpredictable climate events—including localized heatwaves, monsoon downpours, severe storm gusts, and lightning strikes—severely amplify electrical and mechanical degradation.
- **High Consequence of Failure:** A single catastrophic transformer failure can cascade into city-wide blackout events, disrupting critical municipal services (hospitals, water pumping, emergency transport) and causing millions in economic losses.

---

## 2. Key Industry Pain Points

### A. Reactive & Calendar-Based Maintenance Inefficiencies
Traditional distribution utilities rely primarily on calendar-based (time-scheduled) maintenance intervals or reactive firefighting after an outage occurs. 
- *Consequence:* Healthy equipment is over-serviced at high cost, while rapidly deteriorating equipment fails silently between scheduled visits.

### B. Siloed, Unintegrated Telemetry Streams
Modern substations generate millions of sensor data points (dissolved gas analysis, thermal scans, vibration RMS, partial discharge acoustic signals, voltage deviation). However:
- Telemetry is fragmented across proprietary SCADA interfaces.
- Real-time weather data is rarely cross-correlated with point-in-time transformer loading.
- Field maintenance logs and historical incident records remain locked in legacy ticketing databases.

### C. Lack of Calibrated Probabilistic Failure Forecasting
Heuristic threshold alerts (e.g., "temperature > 85°C") flood control center operators with false alarms, inducing alert fatigue. 
- Existing tools lack calibrated failure probability forecasting over operational lead times (e.g., 24 to 168 hours).
- Unsupervised sensor anomaly detection is disconnected from forward-looking supervised risk models.

### D. The "Black Box" AI Trust Deficit
Control room dispatchers and utility engineers cannot act on arbitrary machine learning scores without explainability. 
- Without clear risk factor attribution (e.g., "oil decay rate accounts for 35% of failure risk"), dispatchers hesitate to issue emergency crew work orders.
- Operators need natural language operational grounding that translates complex sensor anomalies into actionable maintenance tasks.

### E. Information Gap Between Utilities and Consumers
During impending failures and planned maintenance, consumers and industrial clients receive zero prior notice.
- Lack of transparent consumer-facing advisories leads to customer dissatisfaction, economic downtime for commercial facilities, and uncoordinated emergency response.

---

## 3. The GridGuard AI Mission & Objectives
The objective of **GridGuard AI** (developed for the IBM x BOB Hackathon) is to engineer an enterprise-grade, end-to-end Predictive Maintenance and Power Outage Risk Advisory platform that:
1. **Forecasts Asset Failure:** Delivers calibrated failure probabilities within a 7-day operational horizon using supervised machine learning (XGBoost with Platt calibration).
2. **Detects Subtle Pre-Failure Anomalies:** Continuously monitors multi-channel sensor feeds via multivariate Isolation Forest.
3. **Calculates Multi-Factor Composite Risk:** Fuses failure probability, anomaly severity, weather exposure, historical failure rates, and grid criticality into an IEEE/CIGRE-aligned composite risk score (0–100).
4. **Delivers Explainable AI & LLM Grounding:** Employs tree-based feature attribution and feeds structured, factual context payloads to IBM watsonx.ai (Granite foundation models) for operator guidance.
5. **Optimizes Field Response & Consumer Trust:** Automates P1–P4 maintenance ticket generation with crew dispatch intelligence and provides an intuitive, role-based web interface for both grid operators and affected consumers.
