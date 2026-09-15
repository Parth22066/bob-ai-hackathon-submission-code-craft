@echo off
title GridGuard AI - Startup Launcher
color 0B

echo ===============================================================================
echo                 GRIDGUARD AI - ENTERPRISE OPERATIONS SUITE                     
echo         Predictive Maintenance & Power Outage Risk Advisory System             
echo ===============================================================================
echo.

set ROOT_DIR=%~dp0
cd /d "%ROOT_DIR%"

:: 1. Detect Python Environment
if exist "%ROOT_DIR%venv\Scripts\python.exe" (
    set "PYTHON_EXE=%ROOT_DIR%venv\Scripts\python.exe"
    echo [OK] Virtual environment detected: venv
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        set "PYTHON_EXE=python"
        echo [WARNING] venv not found. Using system Python.
    ) else (
        echo [ERROR] Python not found. Please install Python 3.12+ or set up venv.
        pause
        exit /b 1
    )
)

:: 2. Check Node.js and npm
where npm >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js / npm not detected. Please install Node.js 18+.
    pause
    exit /b 1
)
echo [OK] Node.js and npm detected.

:: 3. Run database migrations
echo.
echo [*] Applying backend database migrations...
"%PYTHON_EXE%" src\backend\manage.py migrate --noinput
if %ERRORLEVEL% neq 0 (
    echo [WARNING] Database migration check returned a non-zero code. Proceeding...
)

:: 4. Start Django Backend Server
echo.
echo [*] Launching Django Backend Server on http://localhost:8000 ...
start "GridGuard Backend (Django - Port 8000)" cmd /k "cd /d "%ROOT_DIR%src\backend" && "%PYTHON_EXE%" manage.py runserver 0.0.0.0:8000"

:: 5. Start React Vite Frontend Server
echo [*] Launching React Vite Frontend on http://localhost:5173 ...
start "GridGuard Frontend (Vite - Port 5173)" cmd /k "cd /d "%ROOT_DIR%src\frontend" && npm run dev"

:: 6. Brief pause and launch browser
echo.
echo [*] Waiting for services to initialize...
timeout /t 3 /nobreak >nul

echo [*] Launching GridGuard AI in your default browser...
start http://localhost:5173

echo.
echo ===============================================================================
echo                     GRIDGUARD AI IS NOW RUNNING                                
echo ===============================================================================
echo   - Frontend Portal:    http://localhost:5173
echo   - Backend REST APIs:  http://localhost:8000/api/
echo   - Django Admin:       http://localhost:8000/admin/
echo   - ML Inference Engine: Integrated directly with Django backend
echo.
echo   Demo Accounts:
echo     * Operator (Admin): admin@gridguard.ai  /  admin123
echo     * Consumer (User):  user@gridguard.ai   /  user123
echo.
echo   To stop all running services, run 'stop.bat'.
echo ===============================================================================
echo.
pause
