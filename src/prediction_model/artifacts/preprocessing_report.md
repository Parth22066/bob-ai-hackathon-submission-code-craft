# GridGuard AI — Preprocessing Pipeline Verification Report

**Fitted Pipeline Artifact:** `artifacts\fitted_preprocessing_pipeline.joblib`  
**Pipeline Implementation:** Scikit-Learn `ColumnTransformer` + `RobustScaler` + `SimpleImputer` + `OneHotEncoder`  
**Execution Timestamp:** 2026-09-15T20:40:35.098924  

---

## 1. Time-Aware Dataset Partitioning

To strictly prevent data leakage from future observations, the dataset was partitioned chronologically:

| Split | Time Window | Sample Count | % of Dataset | Failures ($y=1$) | Failure Rate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Train** | `2026-04-18 00:00:00` to `2026-08-01T00:00:00.000000` | 37,860 | 70.0% | 334 | 0.88% |
| **Validation** | `2026-08-01T00:00:00.000000` to `2026-08-23T12:00:00.000000` | 8,100 | 15.0% | 64 | 0.79% |
| **Test** | `2026-08-23T12:00:00.000000` to `2026-09-15 00:00:00` | 8,100 | 15.0% | 0 | 0.00% |
| **Total** | Full 150-Day Period | 54,060 | 100.0% | 398 | 0.74% |

---

## 2. Missing Value Analysis & Resolution

| Feature Name | Missing Count (Raw) | Missing % (Raw) | Missing Count (Post-Pipeline) | Resolution Strategy |
| :--- | :---: | :---: | :---: | :--- |
| `sensor_temperature` | 209 | 0.39% | 0 | Median Imputation (Learned from Train) |
| `sensor_vibration` | 201 | 0.37% | 0 | Median Imputation (Learned from Train) |
| `sensor_partial_discharge` | 231 | 0.43% | 0 | Median Imputation (Learned from Train) |
| `sensor_oil_quality` | 197 | 0.36% | 0 | Median Imputation (Learned from Train) |
| `sensor_asset_health` | 209 | 0.39% | 0 | Median Imputation (Learned from Train) |

- **Total NaNs in Transformed Train Split:** 0
- **Total NaNs in Transformed Validation Split:** 0
- **Total NaNs in Transformed Test Split:** 0
- **Imputation Status:** 100% complete and verified.

---

## 3. Outlier Handling & Clipping

- **Total Outliers Detected via Domain Bounds:** 367 records.
- **Outlier Breakdown by Channel:**
  - `sensor_oil_quality`: 367 extreme sensor readings clipped
- **Handling Strategy:** `DomainOutlierClipper` learned empirical percentiles ($0.2%$ and $99.8%$) exclusively on the training split, clipping extreme sensor spikes without leaking test distribution bounds.

---

## 4. Final Transformed Feature Matrix (50 Features)

The end-to-end pipeline outputs a normalized, numerical feature matrix ready for any estimator:

### Numerical & Engineered Features (41):
- `criticality`
- `age`
- `capacity_load_importance`
- `sensor_temperature`
- `sensor_vibration`
- `sensor_partial_discharge`
- `sensor_oil_quality`
- `sensor_asset_health`
- `weather_temperature`
- `weather_rainfall`
- `weather_wind_speed`
- `weather_humidity`
- `weather_storm_risk`
- `historical_previous_failures`
- `historical_outage_history`
- `historical_maintenance_count`
- `historical_days_since_maintenance`
- `temp_mean_24h`
- `temp_max_24h`
- `temp_std_24h`
- `temp_change_24h`
- `temp_trend_24h`
- `thermal_headroom`
- `vibration_mean_24h`
- `vibration_max_24h`
- `vibration_rms_24h`
- `vibration_change_24h`
- `vibration_crest_factor_24h`
- `pd_mean_24h`
- `pd_max_24h`
- `pd_change_24h`
- `pd_spike_count_72h`
- `oil_quality_decay_7d`
- `temperature_zscore`
- `vibration_zscore`
- `partial_discharge_zscore`
- `oil_quality_zscore`
- `asset_health_zscore`
- `thermal_load_ratio`
- `overdue_maintenance_flag`
- `weather_severity_index`

### One-Hot Encoded Categorical Features (9):
- `asset_type_Circuit Breaker`
- `asset_type_Distribution Transformer`
- `asset_type_Feeder Line`
- `asset_type_Power Transformer`
- `location_Substation Central (SUB-04)`
- `location_Substation East (SUB-02)`
- `location_Substation North (SUB-01)`
- `location_Substation South (SUB-05)`
- `location_Substation West (SUB-03)`

---

## 5. Anti-Leakage Verification Checklist

- [x] **Temporal Partitioning:** Train, validation, and holdout splits are strictly chronological; future timestamps never enter training folds.
- [x] **Transformer Isolation:** All scalers, imputers, and encoders are fitted **strictly on the training split**.
- [x] **Rolling Features Lookback:** Rolling window features for temperature, vibration, and partial discharge only look backward in time ($\le t$).
- [x] **Categorical Encoding:** `OneHotEncoder(handle_unknown='ignore')` avoids crashing on previously unseen categories in production inference.
- [x] **Inference Parity:** The serialized `fitted_preprocessing_pipeline.joblib` applies the exact same transformations to new incoming telemetry streams.
