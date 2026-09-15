# GridGuard AI — Machine Learning Dataset Data Dictionary

## Overview
This data dictionary defines all fields in `gridguard_ml_dataset.csv`, generated for **GridGuard AI** (AI-Powered Predictive Maintenance & Power Outage Risk Advisor). It models realistic electrical grid telemetry conforming to **IEEE Std C57.91** thermal dynamics, **Arrhenius** insulation decay, and multivariate degradation physics.

- **Primary File:** `data/gridguard_ml_dataset.csv`
- **Total Records:** 54,060
- **Assets Monitored:** 60 grid components across 5 substations
- **Temporal Resolution:** 4-hour observations over 150 days
- **Prediction Horizon ($H$):** 168 hours (7 days)

---

## Field Specifications

| Category | Column Name | Data Type | Physical Unit | Valid Range | Missing % | Description & Physical Realism |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Temporal** | `timestamp` | ISO-8601 String | UTC Timestamp | 2026-04-18 to 2026-09-15 | 0.0% | Observation cutoff timestamp at 4-hour intervals. |
| **Asset** | `asset_id` | String | Categorical ID | EQ-001 to EQ-060 | 0.0% | Unique asset identifier. |
| **Asset** | `asset_type` | String | Categorical | Power Transformer, Distribution Transformer, Circuit Breaker, Feeder Line | 0.0% | Functional category of electrical equipment. |
| **Asset** | `location` | String | Substation Name | 5 regional substations | 0.0% | Geographical location / parent substation. |
| **Asset** | `criticality` | Integer | Ordinal Tier (1-4) | 1 to 4 | 0.0% | Operational criticality (1=Low, 2=Med, 3=High, 4=Mission-Critical). **Independently assigned; does NOT leak failure target.** |
| **Asset** | `age` | Float | Years | 1.5 to 35.0 | 0.0% | Equipment chronological service life. Higher age correlates with baseline wear and maintenance needs. |
| **Asset** | `capacity_load_importance`| Float | MVA | 10.0 to 120.0 | 0.0% | Rated transformer/feeder apparent power capacity. Drives thermal load rise. |
| **Sensor** | `sensor_temperature` | Float | °C | -15.0 to 148.0 (Normal: 40-75) | ~2.0% | Winding/oil operating temperature. Coupled to ambient temperature, diurnal load, and internal degradation. Contains realistic outliers/glitches. |
| **Sensor** | `sensor_vibration` | Float | mm/s (RMS) | 0.8 to 80.0 (Normal: 1.2-3.0) | ~2.0% | Mechanical structural vibration. Increases under core looseness, mechanical wear, storm winds, and pre-failure states. |
| **Sensor** | `sensor_partial_discharge`| Float | pC (picoCoulombs)| 5.0 to 1800.0 (Normal: 15-40)| ~2.0% | Dielectric ionization discharge pulses. Bursts exponentially during insulation breakdown. Contains occasional non-damaging grid switching spikes. |
| **Sensor** | `sensor_oil_quality` | Float | Index (0-100) | 12.0 to 98.0 (Normal: 80-98) | ~2.0% | Chemical dielectric breakdown index (proxy for dissolved gases / dielectric strength). Decays via Arrhenius thermal kinetics. |
| **Sensor** | `sensor_asset_health` | Float | Index (0-100) | 5.0 to 100.0 (Normal: 85-98) | ~2.0% | Composite multi-sensor condition index reflecting overall asset state. |
| **Weather** | `weather_temperature` | Float | °C | 18.0 to 44.0 | 0.0% | Local ambient temperature including diurnal cycles and seasonal heat waves. |
| **Weather** | `weather_rainfall` | Float | mm | 0.0 to 110.0 | 0.0% | Precipitation volume over preceding observation window. |
| **Weather** | `weather_wind_speed` | Float | km/h | 5.0 to 95.0 | 0.0% | Sustained wind velocity. Heavy gusts induce structural vibration and tree contact risks. |
| **Weather** | `weather_humidity` | Float | % | 38.0 to 99.0 | 0.0% | Relative air humidity. Elevated (>85%) during storm episodes. |
| **Weather** | `weather_storm_risk` | Float | Normalized [0, 1] | 0.0 to 1.0 | 0.0% | Composite environmental severity index combining high wind, torrential rain, and storm warnings. |
| **Historical**| `historical_previous_failures` | Integer | Count | 0 to 8 | 0.0% | Lifetime count of past breakdown incidents experienced by the asset. |
| **Historical**| `historical_outage_history` | Float | Hours | 0.0 to 85.0 | 0.0% | Cumulative historical service outage hours attributable to this asset. |
| **Historical**| `historical_maintenance_count` | Integer | Count | 0 to 22 | 0.0% | Total completed maintenance work orders over lifetime. |
| **Historical**| `historical_days_since_maintenance` | Float | Days | 0.5 to 180.0 | 0.0% | Elapsed days since last completed maintenance. Recent maintenance suppresses near-term failure probability. |
| **TARGET** | `failure_within_horizon` | Binary (0 / 1) | Indicator | 0 or 1 | 0.0% | **Target Variable:** 1 if asset experiences an unplanned functional breakdown in the forward 168-hour (7-day) window, 0 otherwise. Non-trivially separable. |

---

## Key Realistic Coupling Behaviors
1. **Thermal-Dielectric Kinetics:** Sustained operating temperatures above 65°C accelerate oil degradation according to chemical Arrhenius aging rates.
2. **Pre-Failure Sensor Signatures:** Incipient failure periods display concurrent partial discharge surge (>150 pC), elevated vibration (>4.0 mm/s), and collapsing oil quality (<50.0).
3. **Storm Compounding:** Extreme storms (`weather_storm_risk` > 0.6) increase mechanical vibration and elevate failure hazard on vulnerable/degraded assets.
4. **Maintenance Suppression:** When `historical_days_since_maintenance` is low (<25 days), insulation oil is restored and failure probability is physically reduced.
5. **No Criticality Target Leakage:** Pearson correlation between `criticality` and `failure_within_horizon` is near zero ($r pprox 0.00$), ensuring the model learns physical degradation dynamics rather than spurious administrative labels.
