# Setup & Deployment Guide: GridGuard AI

This document provides complete instructions for setting up, running, testing, and verifying the **GridGuard AI** platform on local development environments and cloud workstations.

---

## 1. System Prerequisites

Before starting, ensure the following runtimes are installed on your workstation:
- **Operating System:** Windows 10/11, macOS, or Linux
- **Python:** Python 3.12 or 3.14 (64-bit)
- **Node.js:** Node.js v18.0.0 or later (v24 LTS recommended)
- **Package Manager:** npm (v9+) or pnpm / yarn

---

## 2. Quick Start: One-Click Windows Automation

For Windows environments, automated batch scripts manage the entire runtime:

### Starting All Services
Simply double-click `start.bat` in the repository root (or run from PowerShell / Command Prompt):
```cmd
start.bat
```
*What `start.bat` does automatically:*
1. Detects and activates the root Python virtual environment (`venv/`).
2. Verifies Node.js and npm availability.
3. Applies any pending Django database migrations (`python manage.py migrate`).
4. Launches the Django REST backend server in a dedicated window on `http://localhost:8000`.
5. Launches the React Vite frontend in a dedicated window on `http://localhost:5173`.
6. Opens `http://localhost:5173` in your default web browser.

### Stopping All Services
To cleanly terminate both servers and free ports 8000 and 5173:
```cmd
stop.bat
```

---

## 3. Manual Step-by-Step Setup

If you prefer launching services manually or are running on macOS/Linux:

### Step A: Python Virtual Environment Setup
```bash
# In repository root
python -m venv venv

# Activate on Windows:
.\venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate

# Install dependencies:
pip install -r src/prediction_model/requirements.txt
pip install django django-cors-headers djangorestframework requests ibm_watsonx_ai python-pptx pytest
```

### Step B: Backend Initialization
```bash
cd src/backend

# Verify Django configuration
python manage.py check

# Run migrations
python manage.py migrate

# Start backend server
python manage.py runserver 0.0.0.0:8000
```
The backend API is now accessible at `http://localhost:8000/api/`.

### Step C: Frontend Initialization
```bash
cd src/frontend

# Install dependencies (if first time)
npm install

# Run Vite dev server
npm run dev
```
The frontend portal is now accessible at `http://localhost:5173`.

---

## 4. Default Demo Accounts

GridGuard AI comes pre-configured with two demo role personas for presentation and testing:

| Role | Email | Password | Access / Portal |
|---|---|---|---|
| **Grid Operations Administrator** | `admin@gridguard.ai` | `admin123` | Full control center: Dashboard, Risk Analysis, Sensors, Weather, Maintenance, Crew, AI Assistant |
| **Consumer / Resident** | `user@gridguard.ai` | `user123` | Consumer transparency hub: Live service status, localized outage alerts, issue reporting, customer AI |

---

## 5. Verification & Automated Test Suites

### A. Machine Learning Tests (`pytest`)
To run unit and integration tests across feature extractors, cross-validation splitters, and model inference:
```bash
cd src/prediction_model
python -m pytest tests/ -v
```

### B. Live Inference Validation
To verify end-to-end model scoring on an arbitrary asset:
```bash
cd src/prediction_model
python scripts/predict.py --asset-id EQ-001
```

### C. Backend Django Health Check
```bash
cd src/backend
python manage.py check
```

### D. Frontend Production Build Check
```bash
cd src/frontend
npm run build
```

---

## 6. External Service Configurations (Optional)

GridGuard AI features self-contained offline mock and fallback capabilities. To enable live external cloud services:

### A. IBM watsonx.ai Foundation Models
In `src/backend/gridguard/settings.py` (or via environment variables):
```python
IBM_WATSONX_APIKEY = "YOUR_IBM_CLOUD_API_KEY"
IBM_WATSONX_PROJECT_ID = "YOUR_WATSONX_PROJECT_ID"
IBM_WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
```

### B. OpenWeather Real-Time Weather
In `src/backend/gridguard/settings.py`:
```python
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
```

---

## 7. Troubleshooting

- **Port 8000 or 5173 already in use:**
  Run `stop.bat` to terminate any hanging background processes, or manually inspect with `netstat -ano | findstr :8000`.
- **CORS Issues:**
  Ensure `django-cors-headers` is listed in `INSTALLED_APPS` and `corsheaders.middleware.CorsMiddleware` is at the very top of `MIDDLEWARE` in `settings.py`.
- **ModuleNotFoundError: No module named 'yaml':**
  Ensure you are using `venv\Scripts\python.exe` which has `pyyaml` installed.
