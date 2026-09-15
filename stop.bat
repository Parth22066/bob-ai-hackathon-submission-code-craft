@echo off
title GridGuard AI - Graceful Shutdown
color 0C

echo ===============================================================================
echo                 STOPPING GRIDGUARD AI SERVICES                                 
echo ===============================================================================
echo.

:: 1. Terminate Django Backend on port 8000
echo [*] Stopping Django Backend (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
    echo     [Stopped] Killed PID %%a on port 8000.
)

:: 2. Terminate Vite Frontend on port 5173
echo [*] Stopping React Vite Frontend (Port 5173)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5173" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
    echo     [Stopped] Killed PID %%a on port 5173.
)

:: 3. Clean up cmd windows titled GridGuard
taskkill /FI "WINDOWTITLE eq GridGuard Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq GridGuard Frontend*" /F >nul 2>&1

echo.
echo ===============================================================================
echo            ALL GRIDGUARD AI SERVICES HAVE BEEN STOPPED                         
echo ===============================================================================
echo.
pause
