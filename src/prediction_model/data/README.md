# GridGuard AI — Telemetry & Predictive Maintenance Dataset

> [!NOTE]
> **Data Nature & Compliance Statement (GridGuard AI SRS v1.1 Section 13):**  
> *"The prototype may use publicly available, simulated, or historical data if live utility data is unavailable; external data sources shall be documented."*  
> Because live electrical transmission & substation telemetry is proprietary and classified as Critical Energy Infrastructure Information (CEII), this dataset has been synthesized using **physics-grounded engineering models** rather than simplistic random noise.

---

## 1. Physics-Grounded Simulation Principles

Rather than generating independent random numbers for each column, this dataset models the interdependencies between environmental conditions, electrical load cycles, and physical degradation dynamics:

1. **Transformer Thermal Kinetics (IEEE Std C57.91):**
   Operating temperature is modeled by:
   $$T_{\text{sensor}} = T_{\text{weather}} + \Delta T_{\text{load}} + \Delta T_{\text{degradation}} + \Delta T_{\text{ambient\_stress}} + \epsilon_T$$
   Where:
   - $\Delta T_{\text{load}}$ follows diurnal power consumption curves (peaking at 14:00 and 20:00).
   - $\Delta T_{\text{degradation}}$ accumulates non-linearly during incipient insulation breakdown.
2. **Dielectric Insulation Aging (Arrhenius Chemical Rate Equation):**
   Transformer oil quality deteriorates according to thermal aging kinetics:
   $$\frac{d(\text{oil\_quality})}{dt} \propto - \exp\left(\frac{T - T_0}{15}\right)$$
   Sustained high temperatures exponentially accelerate oil breakdown.
3. **Partial Discharge (PD) Burst Signatures:**
   In normal operational states, partial discharge remains at a low baseline (15–40 pC). Approaching insulation collapse, high-frequency ionization bursts surge between 150 pC and 700 pC. Occasional transient grid switching pulses appear without causing breakdown (modeling real-world false alarms).
4. **Mechanical Vibration Stress:**
   Baseline vibration (1.2–2.2 mm/s RMS) increases gradually with structural looseness and core wear (>4.0 mm/s), exacerbated by heavy storm winds.
5. **Multi-Sensor Asset Health Condition Index:**
   A continuous composite index ($0\text{--}100$) reflecting real-time physical condition across thermal, vibration, partial discharge, and chemical degradation dimensions.
6. **Maintenance Reset:**
   Routine or post-failure maintenance resets oil quality, reduces vibration, and suppresses near-term failure probability.
7. **Criticality Independence (Zero Leakage):**
   Asset criticality ($1\text{--}4$) is assigned according to grid topological placement and customer sensitivity (e.g. hospital supply vs. rural feeder). It has **zero mathematical correlation** with physical breakdown ($r \approx -0.01$), preventing artificial model leakage.

---

## 2. Dataset Files Summary

| File Path | Description | Format |
| :--- | :--- | :--- |
| `data/gridguard_ml_dataset.csv` | Unified ML-ready tabular dataset | CSV (54,060 rows, 22 columns) |
| `data/data_dictionary.md` | Exhaustive field descriptions, units, ranges, and physical meanings | Markdown |
| `data/dataset_statistics.json` | Statistical summary (mean, std, percentiles, correlations, missingness) | JSON |
| `data/target_distribution_report.md` | Class imbalance, failure breakdown by asset type/criticality, and feature separation | Markdown |
| `artifacts/plots/correlation_matrix.png` | Feature-to-feature and feature-to-target correlation heatmap | PNG |
| `artifacts/plots/sensor_distributions_by_target.png` | Distribution comparisons between normal ($y=0$) and failing ($y=1$) states | PNG |
| `artifacts/plots/temporal_degradation_profile.png` | Multi-channel degradation trajectory comparing a failing vs normal asset | PNG |
| `artifacts/plots/weather_and_storm_impact.png` | Substation environmental timeline showing ambient temp, rainfall, and storm risk | PNG |

---

## 3. Dataset Profile & Target Formulation

- **Assets:** 60 electrical grid assets (Power Transformers, Distribution Transformers, Circuit Breakers, Feeder Lines) across 5 substations.
- **Timeline:** 150 days (April 18, 2026 to September 15, 2026).
- **Sampling Cadence:** Every 4 hours ($54,060$ total observations).
- **Prediction Horizon ($H$):** 168 hours (7 days forward hazard window).
- **Target Variable (`failure_within_horizon`):**
  - **Class 0 (Normal):** $53,662$ records ($99.26\%$)
  - **Class 1 (Failing within 7 days):** $398$ records ($0.74\%$)
- **Data Imperfections Included:**
  - ~2.0% realistic missing values across sensor streams (simulating IoT packet loss).
  - ~0.5% isolated sensor glitches and transient spikes.
  - Non-trivial overlap between normal and pre-failure distributions.

---

## 4. How to Regenerate the Dataset

You can regenerate the benchmark dataset or produce alternate scenarios using `data/synthetic_generator.py`:

```bash
# Standard 60-asset, 150-day dataset with seed 42
python data/synthetic_generator.py --assets 60 --days 150 --interval 4 --seed 42 --output-dir data

# Generate reports and data dictionary
python scripts/generate_dataset_reports.py

# Generate visualization plots
python scripts/visualize_dataset.py
```
