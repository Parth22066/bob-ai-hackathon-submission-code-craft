"""
Dataset visualization script for GridGuard AI.
Generates publication-quality figures illustrating sensor degradation,
correlation heatmaps, target distributions, and temporal failure trajectories.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg") # Non-interactive headless backend
import matplotlib.pyplot as plt

def generate_visualizations():
    plots_dir = Path("artifacts/plots")
    plots_dir.mkdir(parents=True, exist_ok=True)
    
    csv_path = Path("data/gridguard_ml_dataset.csv")
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found at {csv_path}")
        
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Set styling
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    plt.rcParams.update({"font.size": 10, "axes.labelsize": 11, "figure.titlesize": 13})
    
    # -----------------------------------------------------------------
    # 1. CORRELATION HEATMAP
    # -----------------------------------------------------------------
    print("[1/4] Generating Correlation Heatmap...")
    feature_cols = [
        "sensor_temperature", "sensor_vibration", "sensor_partial_discharge",
        "sensor_oil_quality", "sensor_asset_health", "weather_temperature",
        "weather_rainfall", "weather_wind_speed", "weather_storm_risk",
        "historical_previous_failures", "historical_days_since_maintenance",
        "criticality", "age", "failure_within_horizon"
    ]
    
    corr = df[feature_cols].corr()
    
    fig, ax = plt.subplots(figsize=(11, 9))
    cax = ax.matshow(corr, cmap="coolwarm", vmin=-0.7, vmax=0.7)
    fig.colorbar(cax, fraction=0.046, pad=0.04)
    
    labels = [c.replace("sensor_", "s_").replace("weather_", "w_").replace("historical_", "h_") for c in feature_cols]
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="left")
    ax.set_yticklabels(labels)
    
    # Add text annotations for correlation values
    for i in range(len(labels)):
        for j in range(len(labels)):
            val = corr.iloc[i, j]
            color = "white" if abs(val) > 0.45 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=8)
            
    plt.title("GridGuard AI: Feature Correlation Matrix", pad=30, fontweight="bold")
    plt.tight_layout()
    corr_path = plots_dir / "correlation_matrix.png"
    plt.savefig(corr_path, dpi=200)
    plt.close()
    print(f"  Saved: {corr_path}")

    # -----------------------------------------------------------------
    # 2. SENSOR DISTRIBUTIONS: NORMAL (y=0) VS FAILING (y=1)
    # -----------------------------------------------------------------
    print("[2/4] Generating Sensor Distributions by Target...")
    sensors_to_plot = [
        ("sensor_temperature", "Operating Temperature (°C)", 20, 110),
        ("sensor_vibration", "Vibration (mm/s RMS)", 0.5, 12.0),
        ("sensor_partial_discharge", "Partial Discharge (pC)", 0, 400),
        ("sensor_asset_health", "Asset Health Index (0-100)", 20, 105)
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    axes = axes.ravel()
    
    for idx, (col, title, xmin, xmax) in enumerate(sensors_to_plot):
        ax = axes[idx]
        norm_data = df[df["failure_within_horizon"] == 0][col].dropna()
        fail_data = df[df["failure_within_horizon"] == 1][col].dropna()
        
        # Filter for plotting range to avoid distortion by extreme outliers
        norm_filtered = norm_data[(norm_data >= xmin) & (norm_data <= xmax)]
        fail_filtered = fail_data[(fail_data >= xmin) & (fail_data <= xmax)]
        
        ax.hist(norm_filtered, bins=40, density=True, alpha=0.55, color="#1f77b4", label="Normal (y=0)")
        ax.hist(fail_filtered, bins=40, density=True, alpha=0.65, color="#d62728", label="Failing within 7d (y=1)")
        
        ax.set_title(title, fontweight="bold")
        ax.set_xlabel(title)
        ax.set_ylabel("Probability Density")
        ax.set_xlim(xmin, xmax)
        ax.legend(loc="upper right")
        
    plt.suptitle("Sensor Signatures: Normal vs. Pre-Failure State (Realistic Overlap)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    dist_path = plots_dir / "sensor_distributions_by_target.png"
    plt.savefig(dist_path, dpi=200)
    plt.close()
    print(f"  Saved: {dist_path}")

    # -----------------------------------------------------------------
    # 3. TEMPORAL DEGRADATION TRAJECTORY (FAILING VS NORMAL ASSET)
    # -----------------------------------------------------------------
    print("[3/4] Generating Temporal Degradation Profile...")
    # Find a failing asset and a normal asset
    failing_assets = df[df["failure_within_horizon"] == 1]["asset_id"].unique()
    failing_id = failing_assets[0]
    
    normal_assets = [aid for aid in df["asset_id"].unique() if aid not in failing_assets]
    normal_id = normal_assets[0]
    
    df_fail = df[df["asset_id"] == failing_id].sort_values("timestamp")
    df_norm = df[df["asset_id"] == normal_id].sort_values("timestamp")
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(13, 10), sharex=True)
    
    # 1. Partial Discharge
    ax1.plot(df_norm["timestamp"], df_norm["sensor_partial_discharge"], color="#2ca02c", alpha=0.7, label=f"Normal Asset ({normal_id})")
    ax1.plot(df_fail["timestamp"], df_fail["sensor_partial_discharge"], color="#d62728", linewidth=1.8, label=f"Failing Asset ({failing_id})")
    ax1.set_ylabel("Partial Discharge (pC)")
    ax1.set_title(f"Temporal Degradation Profile: Failing Asset ({failing_id}) vs Normal ({normal_id})", fontweight="bold")
    ax1.legend(loc="upper left")
    
    # 2. Temperature & Vibration
    ax2.plot(df_fail["timestamp"], df_fail["sensor_temperature"], color="#ff7f0e", linewidth=1.6, label="Temperature (°C)")
    ax2_vib = ax2.twinx()
    ax2_vib.plot(df_fail["timestamp"], df_fail["sensor_vibration"], color="#9467bd", linestyle="--", linewidth=1.4, label="Vibration (mm/s)")
    ax2.set_ylabel("Temperature (°C)", color="#ff7f0e")
    ax2_vib.set_ylabel("Vibration (mm/s)", color="#9467bd")
    ax2.legend(loc="upper left")
    ax2_vib.legend(loc="upper right")
    
    # 3. Asset Health & Target Indicator
    ax3.plot(df_fail["timestamp"], df_fail["sensor_asset_health"], color="#1f77b4", linewidth=2.0, label="Asset Health Condition Index")
    ax3_tgt = ax3.twinx()
    ax3_tgt.fill_between(df_fail["timestamp"], 0, df_fail["failure_within_horizon"], color="red", alpha=0.25, label="Failure Hazard Active (y=1)")
    ax3.set_ylabel("Health Index (0-100)", color="#1f77b4")
    ax3_tgt.set_ylabel("Target Indicator (0/1)", color="red")
    ax3_tgt.set_ylim(-0.1, 1.5)
    ax3.set_xlabel("Observation Timeline")
    ax3.legend(loc="lower left")
    ax3_tgt.legend(loc="upper right")
    
    plt.tight_layout()
    traj_path = plots_dir / "temporal_degradation_profile.png"
    plt.savefig(traj_path, dpi=200)
    plt.close()
    print(f"  Saved: {traj_path}")

    # -----------------------------------------------------------------
    # 4. WEATHER & STORM SEVERITY TIMELINE
    # -----------------------------------------------------------------
    print("[4/4] Generating Weather and Storm Impact Timeline...")
    first_sub = df["location"].iloc[0]
    df_sub_weather = df[df["location"] == first_sub].drop_duplicates(subset=["timestamp"]).sort_values("timestamp")
    
    fig, (w1, w2) = plt.subplots(2, 1, figsize=(13, 7), sharex=True)
    
    w1.plot(df_sub_weather["timestamp"], df_sub_weather["weather_temperature"], color="#e377c2", label="Ambient Temp (°C)")
    w1_rain = w1.twinx()
    w1_rain.bar(df_sub_weather["timestamp"], df_sub_weather["weather_rainfall"], width=0.15, color="#17becf", alpha=0.6, label="Precipitation (mm)")
    w1.set_ylabel("Temp (°C)", color="#e377c2")
    w1_rain.set_ylabel("Rainfall (mm)", color="#17becf")
    w1.set_title(f"Environmental Dynamics & Storm Impact ({first_sub})", fontweight="bold")
    w1.legend(loc="upper left")
    w1_rain.legend(loc="upper right")
    
    w2.plot(df_sub_weather["timestamp"], df_sub_weather["weather_wind_speed"], color="#7f7f7f", label="Wind Speed (km/h)")
    w2_risk = w2.twinx()
    w2_risk.plot(df_sub_weather["timestamp"], df_sub_weather["weather_storm_risk"], color="#bcbd22", linewidth=2.0, label="Storm Risk Index (0-1)")
    w2.set_ylabel("Wind Speed (km/h)", color="#7f7f7f")
    w2_risk.set_ylabel("Storm Risk Index", color="#bcbd22")
    w2_risk.set_ylim(-0.05, 1.1)
    w2.set_xlabel("Observation Timeline")
    w2.legend(loc="upper left")
    w2_risk.legend(loc="upper right")
    
    plt.tight_layout()
    weather_path = plots_dir / "weather_and_storm_impact.png"
    plt.savefig(weather_path, dpi=200)
    plt.close()
    print(f"  Saved: {weather_path}")
    print("All visualizations generated successfully.")

if __name__ == "__main__":
    generate_visualizations()
