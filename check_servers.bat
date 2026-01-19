@echo off
REM Simple script to check if servers are running

echo Checking if servers are running...
echo.

echo [1] Checking Backend (port 8000)...
curl -s http://localhost:8000/admin >nul 2>&1
if %errorlevel% equ 0 (
    echo    Backend: RUNNING on http://localhost:8000
) else (
    echo    Backend: NOT RUNNING
    echo    To start: cd backend ^&^& python manage.py runserver
)

echo.
echo [2] Checking Frontend (port 3000)...
curl -s http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo    Frontend: RUNNING on http://localhost:3000
) else (
    echo    Frontend: NOT RUNNING
    echo    To start: cd frontend ^&^& npm start
)

echo.
pause
