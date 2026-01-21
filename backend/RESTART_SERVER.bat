@echo off
echo ================================================
echo   Restarting Django Backend Server
echo ================================================
echo.
echo Stopping any running Django servers...
echo Press Ctrl+C in the terminal running Django
echo.
echo Starting server with timezone fix...
cd /d "%~dp0"
call venv\Scripts\activate.bat
python manage.py runserver
pause
