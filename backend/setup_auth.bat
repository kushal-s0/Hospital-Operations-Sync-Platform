@echo off
REM Quick setup script for authentication
REM Run this from the backend directory

echo ========================================
echo Hospital Information System - Auth Setup
echo ========================================
echo.

echo [1/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [2/3] Running migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)
echo.

echo [3/3] Creating test users...
python create_test_users.py
if errorlevel 1 (
    echo ERROR: Failed to create test users
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now:
echo 1. Start backend: python manage.py runserver
echo 2. Start frontend: cd ../frontend ^&^& npm start
echo 3. Login at http://localhost:3000
echo.
echo Test Credentials:
echo - Username: admin     / Password: admin123
echo - Username: doctor1   / Password: doctor123
echo - Username: nurse1    / Password: nurse123
echo.
pause
