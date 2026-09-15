# GridGuard AI — Source Code Directory

This directory contains the complete source code for GridGuard AI, organized into three decoupled subsystems:

- **`backend/`**: Django 6.1 REST API gateway, database ORM models (`Asset`, `TelemetryLog`, `MaintenanceLog`), live OpenWeather client, and IBM watsonx.ai foundation model connector.
- **`frontend/`**: React 18 + Vite modern single-page application with Tailwind CSS, Recharts time-series telemetry charts, and dual-persona interfaces (Control Center & Citizen Portal).
- **`prediction_model/`**: Machine learning subsystem featuring calibrated XGBoost failure prediction, multivariate Isolation Forest anomaly detection, 35+ point-in-time engineered features, and model registry artifacts.

## Running the Source Code
From the repository root:
- Run `start.bat` for one-click startup.
- See `docs/setup-guide.md` for manual execution instructions.
