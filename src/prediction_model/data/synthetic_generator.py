"""
GridGuard AI — Industrial Predictive Maintenance Synthetic Telemetry Generator.
Version: 2.0 (Physics-grounded, non-trivially separable, IEEE C57.91 & Arrhenius-aligned)

Models realistic relationships between:
- ASSET: asset_id, asset_type, location, criticality, age, capacity_load_importance
- SENSOR: temperature, vibration, partial_discharge, oil_quality, asset_health
- WEATHER: temperature, rainfall, wind_speed, humidity, storm_risk
- HISTORICAL: previous_failures, outage_history, maintenance_count, days_since_maintenance
- TARGET: failure_within_horizon (forward hazard indicator)

Guarantees:
- Criticality does NOT leak the target failure label.
- Realistic temporal degradation and seasonal/diurnal patterns.
- Stochastic survival dynamics (non-trivially separable; avoids artificial 100% accuracy).
- Includes normal, mild degradation, severe degradation, false-alarm anomaly periods,
  sensor packet loss (missing values), measurement noise, and sensor glitch outliers.
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd

def generate_gridguard_dataset(
    num_assets: int = 60,
    days: int = 150,
    sampling_interval_hours: int = 4,
    horizon_hours: int = 168,  # 7 days forward prediction horizon
    random_seed: int = 42,
    missing_rate: float = 0.02,
    glitch_rate: float = 0.005,
    output_dir: Optional[Path] = None
) -> pd.DataFrame:
    """
    Generates a unified, realistic predictive maintenance dataset for GridGuard AI.
    """
    np.random.seed(random_seed)
    
    end_date = datetime(2026, 9, 15, 0, 0)
    start_date = end_date - timedelta(days=days)
    timestamps = pd.date_range(start=start_date, end=end_date, freq=f"{sampling_interval_hours}h")
    n_steps = len(timestamps)
    
    # -------------------------------------------------------------
    # 1. ASSET DEFINITIONS
    # -------------------------------------------------------------
    asset_types = ["Power Transformer", "Distribution Transformer", "Circuit Breaker", "Feeder Line"]
    substations = [
        "Substation North (SUB-01)",
        "Substation East (SUB-02)",
        "Substation West (SUB-03)",
        "Substation Central (SUB-04)",
        "Substation South (SUB-05)"
    ]
    
    assets = []
    for i in range(1, num_assets + 1):
        a_id = f"EQ-{i:03d}"
        a_type = np.random.choice(asset_types, p=[0.35, 0.25, 0.25, 0.15])
        loc = np.random.choice(substations)
        
        # Age: 2 to 32 years (log-normal distribution with older tail)
        age = float(np.clip(np.random.lognormal(mean=2.4, sigma=0.5), 1.5, 35.0))
        
        # Criticality: Tier 1 (Low), Tier 2 (Medium), Tier 3 (High), Tier 4 (Mission Critical)
        # CRITICAL RULE: Criticality reflects grid placement/load importance, NOT physical wear!
        crit = int(np.random.choice([1, 2, 3, 4], p=[0.20, 0.35, 0.30, 0.15]))
        
        # Capacity / load importance: MVA rating (10 to 120 MVA)
        if "Power" in a_type:
            capacity_mva = float(np.random.choice([60.0, 80.0, 100.0, 120.0]))
        elif "Distribution" in a_type:
            capacity_mva = float(np.random.choice([15.0, 25.0, 40.0]))
        else:
            capacity_mva = float(np.random.choice([10.0, 20.0, 30.0]))
            
        # Baseline manufacturing tolerance / individual baseline variability
        base_vib = float(np.random.uniform(1.2, 2.2))
        base_pd = float(np.random.uniform(12.0, 32.0))
        base_oil = float(np.random.uniform(88.0, 98.0))
        
        # Historical profile correlated with age
        prev_failures = int(np.random.poisson(lam=max(0.2, age * 0.12)))
        outage_hours = round(float(prev_failures * np.random.uniform(3.0, 14.0)), 2)
        mnt_count = int(np.random.poisson(lam=max(1.0, age * 0.4)))
        
        # Condition assignment for the simulation timeline:
        # ~70% healthy/normal, ~18% mild degradation, ~12% pre-failure / breakdown
        condition = np.random.choice(
            ["normal", "mild_degradation", "pre_failure"],
            p=[0.70, 0.18, 0.12]
        )
        
        assets.append({
            "asset_id": a_id,
            "asset_type": a_type,
            "location": loc,
            "criticality": crit,
            "age": round(age, 1),
            "capacity_load_importance": capacity_mva,
            "previous_failures": prev_failures,
            "outage_history": outage_hours,
            "maintenance_count": mnt_count,
            "base_vib": base_vib,
            "base_pd": base_pd,
            "base_oil": base_oil,
            "condition": condition,
            "failure_timestamp": None,
            "degradation_start_idx": None,
            "transient_anomaly_idx": None
        })
        
    # Configure degradation timing for failing assets
    for a in assets:
        if a["condition"] == "pre_failure":
            # Schedule failure between day 40 and day 140
            fail_step = np.random.randint(int(n_steps * 0.28), int(n_steps * 0.90))
            a["failure_timestamp"] = timestamps[fail_step]
            # Incipient degradation begins 4 to 12 days before breakdown
            deg_steps = int(np.random.uniform(4, 12) * 24 / sampling_interval_hours)
            a["degradation_start_idx"] = max(0, fail_step - deg_steps)
        elif a["condition"] == "normal":
            # 15% of normal assets experience transient false-alarm anomalies (vibration/PD spikes that resolve)
            if np.random.rand() < 0.15:
                a["transient_anomaly_idx"] = np.random.randint(int(n_steps * 0.2), int(n_steps * 0.8))
                
    # -------------------------------------------------------------
    # 2. WEATHER TIME-SERIES PER SUBSTATION
    # -------------------------------------------------------------
    weather_dict = {}
    for sub in substations:
        base_temp = np.random.uniform(25.0, 30.0)
        # Pre-plan 2-4 storm fronts per substation
        storms = []
        for _ in range(np.random.randint(2, 5)):
            s_start = np.random.randint(10, n_steps - 20)
            s_len = np.random.randint(3, 10) # 12h to 40h
            storms.append((s_start, s_start + s_len))
            
        sub_weather = []
        for t_idx, ts in enumerate(timestamps):
            hour = ts.hour
            doy = ts.dayofyear
            # Diurnal sinusoidal cycle + day-to-day drift
            diurnal = 5.5 * np.sin(2 * np.pi * (hour - 9) / 24.0)
            seasonal_drift = 2.0 * np.sin(2 * np.pi * (doy - 100) / 365.0)
            amb_temp = base_temp + diurnal + seasonal_drift + np.random.normal(0, 1.2)
            
            # Check storm activity
            in_storm = any(s[0] <= t_idx <= s[1] for s in storms)
            if in_storm:
                rain = np.random.exponential(18.0) + 6.0
                wind = np.random.uniform(48.0, 88.0)
                humidity = np.random.uniform(86.0, 99.0)
                # Storm risk index: 0.65 to 1.0 during active severe storms
                storm_risk = float(np.clip(0.60 + (wind / 180.0) + (rain / 200.0) + np.random.normal(0, 0.05), 0.6, 1.0))
            else:
                rain = np.random.exponential(0.6) if np.random.rand() < 0.08 else 0.0
                wind = np.random.uniform(6.0, 26.0)
                humidity = np.random.uniform(42.0, 72.0)
                storm_risk = float(np.clip((wind / 120.0) + (rain / 150.0) + np.random.normal(0, 0.03), 0.0, 0.45))
                
            sub_weather.append({
                "weather_temperature": round(amb_temp, 2),
                "weather_rainfall": round(rain, 2),
                "weather_wind_speed": round(wind, 2),
                "weather_humidity": round(humidity, 1),
                "weather_storm_risk": round(storm_risk, 3)
            })
        weather_dict[sub] = sub_weather

    # -------------------------------------------------------------
    # 3. COMBINED OBSERVATIONS & TEMPORAL SIMULATION
    # -------------------------------------------------------------
    rows = []
    
    for a in assets:
        loc = a["location"]
        sub_w = weather_dict[loc]
        cap = a["capacity_load_importance"]
        condition = a["condition"]
        fail_ts = a["failure_timestamp"]
        deg_start = a["degradation_start_idx"]
        transient_idx = a["transient_anomaly_idx"]
        
        # Days since last maintenance tracker
        # Initialize with realistic random past service (10 to 110 days ago)
        initial_days_since_mnt = float(np.random.uniform(10.0, 110.0))
        
        # Track progressive degradation state
        oil_state = a["base_oil"]
        
        for t_idx, ts in enumerate(timestamps):
            w = sub_w[t_idx]
            amb_temp = w["weather_temperature"]
            storm_risk = w["weather_storm_risk"]
            
            # Days since maintenance advances
            elapsed_days = (ts - start_date).total_seconds() / 86400.0
            current_days_since_mnt = initial_days_since_mnt + elapsed_days
            
            # Reset maintenance if scheduled maintenance occurred
            # Routine maintenance every ~90 days for well-managed assets
            if current_days_since_mnt > 105.0 and condition != "pre_failure":
                current_days_since_mnt = float(np.random.uniform(0.5, 4.0))
                oil_state = a["base_oil"] # Oil refreshed
                
            # If asset failed in the past, post-failure maintenance restored it
            if fail_ts is not None and ts > fail_ts:
                # Restored to service
                condition_now = "normal"
                current_days_since_mnt = float((ts - fail_ts).total_seconds() / 86400.0)
                progress = 0.0
            elif fail_ts is not None and t_idx >= deg_start:
                condition_now = "pre_failure"
                # Exponential/polynomial degradation trajectory
                total_deg_steps = max(1, (fail_ts - timestamps[deg_start]).total_seconds() / (sampling_interval_hours * 3600.0))
                elapsed_deg_steps = max(0, t_idx - deg_start)
                progress = min(1.0, elapsed_deg_steps / total_deg_steps)
            elif condition == "mild_degradation":
                condition_now = "mild_degradation"
                progress = float(min(0.55, 0.15 + (elapsed_days / days) * 0.4))
            else:
                condition_now = "normal"
                progress = 0.0
                
            # Load current dynamics (diurnal demand peaking at 2 PM and 8 PM)
            hour = ts.hour
            diurnal_load = 0.65 + 0.30 * np.sin(2 * np.pi * (hour - 6) / 24.0)**2
            load_factor = diurnal_load + np.random.normal(0, 0.04)
            
            # 1. SENSOR: TEMPERATURE
            # IEEE Std C57.91 heating equation: AmbTemp + delta_T_rated * (Load/Rated)^1.6
            rated_temp_rise = 32.0 * (cap / 100.0)**0.25
            thermal_load_rise = rated_temp_rise * (load_factor**1.6)
            
            thermal_deg_penalty = 38.0 * (progress**1.8) if condition_now == "pre_failure" else (10.0 * progress)
            # High ambient / heat wave compounding
            ambient_stress = max(0.0, (amb_temp - 34.0) * 1.2)
            
            temp_val = amb_temp + thermal_load_rise + thermal_deg_penalty + ambient_stress + np.random.normal(0, 1.4)
            
            # 2. SENSOR: VIBRATION
            # Base vibration + load harmonics + mechanical defect trajectory + storm wind vibration
            vib_deg = (7.5 * (progress**2.0)) if condition_now == "pre_failure" else (1.4 * progress)
            wind_vibration = 0.015 * w["weather_wind_speed"]
            vib_val = a["base_vib"] + vib_deg + wind_vibration + np.random.normal(0, 0.18)
            
            # Transient vibration anomaly (false alarm / external construction / grid switching)
            if transient_idx is not None and abs(t_idx - transient_idx) <= 2:
                vib_val += np.random.uniform(4.0, 7.5) # temporary spike
                
            # 3. SENSOR: PARTIAL DISCHARGE (pC)
            # Normal: 15-40 pC; Failing: 150-700 pC bursts
            pd_deg = (420.0 * (progress**2.6)) if condition_now == "pre_failure" else (35.0 * progress)
            pd_val = a["base_pd"] + pd_deg + np.random.normal(0, 4.0)
            
            # Occasional transient electromagnetic pulse / grid switching surge
            if np.random.rand() < 0.015 and condition_now == "normal":
                pd_val += np.random.uniform(60.0, 140.0) # spurious transient spike
            pd_val = max(5.0, pd_val)
            
            # 4. SENSOR: OIL QUALITY INDEX (0 to 100)
            # Arrhenius degradation: sustained heat accelerates oil decay
            daily_decay = 0.03 * np.exp(max(0.0, (temp_val - 60.0) / 15.0))
            if condition_now == "pre_failure":
                daily_decay += 2.5 * (progress**1.5)
            oil_state = max(12.0, oil_state - daily_decay * (sampling_interval_hours / 24.0) + np.random.normal(0, 0.15))
            oil_val = round(oil_state, 1)
            
            # 5. SENSOR: ASSET HEALTH INDEX (0 to 100)
            # Multi-sensor continuous condition index (100 = brand new, <40 = critical degradation)
            t_pen = min(35.0, max(0.0, (temp_val - 65.0) * 1.2))
            v_pen = min(25.0, max(0.0, (vib_val - 2.8) * 5.0))
            pd_pen = min(25.0, max(0.0, (pd_val - 50.0) * 0.12))
            oil_pen = min(25.0, max(0.0, (85.0 - oil_val) * 0.4))
            health_val = max(5.0, min(100.0, 100.0 - (t_pen + v_pen + pd_pen + oil_pen) + np.random.normal(0, 1.5)))
            
            # ---------------------------------------------------------
            # 4. TARGET: FAILURE WITHIN PREDICTION HORIZON (7 DAYS)
            # ---------------------------------------------------------
            # Forward Hazard Formulation:
            # Does this asset suffer a functional failure event in (ts, ts + H]?
            #
            # STOCHASTIC HAZARD LOG-ODDS:
            # Failure is a physical outcome driven by sensor stress, aging, oil decay,
            # weather storms, and lack of maintenance.
            # CRITICALITY has 0.0 coefficient (does NOT cause failure!).
            
            horizon_end = ts + timedelta(hours=horizon_hours)
            
            if fail_ts is not None and ts < fail_ts <= horizon_end:
                # Scheduled breakdown falls inside the forward horizon
                target = 1
            else:
                # Stochastic background hazard:
                # Allows for occasional unexpected breakdown or false alarm resilience
                z_hazard = (
                    -6.2
                    + 0.055 * (temp_val - 65.0)
                    + 0.55 * (vib_val - 3.0)
                    + 0.012 * (pd_val - 60.0)
                    + 0.045 * (75.0 - oil_val)
                    + 0.04 * (a["age"] - 15.0)
                    + 1.8 * storm_risk
                    + 0.25 * a["previous_failures"]
                    - 0.8 * np.exp(-current_days_since_mnt / 25.0)
                    + np.random.normal(0, 0.4) # unobserved latent disturbance
                )
                p_stochastic_failure = 1.0 / (1.0 + np.exp(-z_hazard))
                
                # If background hazard exceeds random threshold, stochastic failure happens
                target = 1 if (np.random.rand() < p_stochastic_failure and current_days_since_mnt > 5.0) else 0

            # ---------------------------------------------------------
            # 5. DATASET REALISM: MISSING VALUES & SENSOR GLITCHES
            # ---------------------------------------------------------
            t_final = temp_val
            v_final = vib_val
            pd_final = pd_val
            oil_final = oil_val
            h_final = health_val
            
            # Sensor glitches (isolated extreme outlier)
            if np.random.rand() < glitch_rate:
                which_sensor = np.random.choice(["temp", "vib", "pd"])
                if which_sensor == "temp":
                    t_final = float(np.random.choice([-15.0, 148.0]))
                elif which_sensor == "vib":
                    v_final = float(np.random.uniform(45.0, 80.0))
                elif which_sensor == "pd":
                    pd_final = float(np.random.uniform(900.0, 1800.0))
                    
            # Missing values (IoT transmission packet dropout)
            if np.random.rand() < missing_rate:
                drop_col = np.random.choice(["temperature", "vibration", "partial_discharge", "oil_quality", "asset_health"])
                if drop_col == "temperature": t_final = np.nan
                elif drop_col == "vibration": v_final = np.nan
                elif drop_col == "partial_discharge": pd_final = np.nan
                elif drop_col == "oil_quality": oil_final = np.nan
                elif drop_col == "asset_health": h_final = np.nan
                
            rows.append({
                "timestamp": ts.isoformat(),
                "asset_id": a["asset_id"],
                "asset_type": a["asset_type"],
                "location": a["location"],
                "criticality": a["criticality"],
                "age": round(a["age"], 1),
                "capacity_load_importance": a["capacity_load_importance"],
                "sensor_temperature": round(t_final, 2) if not np.isnan(t_final) else np.nan,
                "sensor_vibration": round(v_final, 3) if not np.isnan(v_final) else np.nan,
                "sensor_partial_discharge": round(pd_final, 1) if not np.isnan(pd_final) else np.nan,
                "sensor_oil_quality": round(oil_final, 1) if not np.isnan(oil_final) else np.nan,
                "sensor_asset_health": round(h_final, 1) if not np.isnan(h_final) else np.nan,
                "weather_temperature": round(w["weather_temperature"], 2),
                "weather_rainfall": round(w["weather_rainfall"], 2),
                "weather_wind_speed": round(w["weather_wind_speed"], 2),
                "weather_humidity": round(w["weather_humidity"], 1),
                "weather_storm_risk": round(w["weather_storm_risk"], 3),
                "historical_previous_failures": a["previous_failures"],
                "historical_outage_history": a["outage_history"],
                "historical_maintenance_count": a["maintenance_count"],
                "historical_days_since_maintenance": round(current_days_since_mnt, 1),
                "failure_within_horizon": int(target)
            })

    df = pd.DataFrame(rows)
    
    # Save outputs if output_dir specified
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        csv_path = output_dir / "gridguard_ml_dataset.csv"
        df.to_csv(csv_path, index=False)
        print(f"Generated unified dataset saved to: {csv_path}")
        print(f"Total records: {len(df):,}")
        print(f"Assets: {num_assets} | Timeline: {days} days ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        print(f"Positive failure class: {df['failure_within_horizon'].sum()} ({df['failure_within_horizon'].mean():.2%})")
        
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GridGuard AI Realistic Synthetic Dataset Generator")
    parser.add_argument("--assets", type=int, default=60, help="Number of electrical grid assets")
    parser.add_argument("--days", type=int, default=150, help="Simulation duration in days")
    parser.add_argument("--interval", type=int, default=4, help="Sampling frequency in hours")
    parser.add_argument("--seed", type=int, default=42, help="Reproducible random seed")
    parser.add_argument("--output-dir", type=str, default="data", help="Output directory")
    args = parser.parse_args()

    generate_gridguard_dataset(
        num_assets=args.assets,
        days=args.days,
        sampling_interval_hours=args.interval,
        random_seed=args.seed,
        output_dir=Path(args.output_dir)
    )
