@echo off
echo ========================================
echo Starting Hospital Information System
echo ========================================
echo.

REM Get the directory of this script
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Start Backend in new window
echo [1/2] Starting Backend Server...
start "HIS Backend" cmd /k "cd /d "%SCRIPT_DIR%backend" && python manage.py runserver"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend in new window
echo [2/2] Starting Frontend...
start "HIS Frontend" cmd /k "cd /d "%SCRIPT_DIR%frontend" && npm start"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Login with:
echo   Username: admin
echo   Password: admin123
echo.
echo Press any key to close this window...
pause >nul
