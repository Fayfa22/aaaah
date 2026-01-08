@echo off
REM MediConnect Setup Script for Windows

echo.
echo ========================================
echo   MediConnect - Healthcare Platform
echo   Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Step 2: Installing dependencies...
pip install -r requirements.txt

echo Step 3: Running database migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To start the application:
echo   1. Activate virtual environment: venv\Scripts\activate.bat
echo   2. Run: python manage.py runserver
echo.
echo Default Access:
echo   - Application: http://127.0.0.1:8000/
echo   - Admin Panel: http://127.0.0.1:8000/admin/
echo.
echo To create a superuser account, run:
echo   python manage.py createsuperuser
echo.
pause
