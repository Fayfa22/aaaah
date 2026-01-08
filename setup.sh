#!/bin/bash

# MediConnect Setup Script for macOS/Linux

echo ""
echo "========================================"
echo "  MediConnect - Healthcare Platform"
echo "  Setup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Step 2: Installing dependencies..."
pip install -r requirements.txt

echo "Step 3: Running database migrations..."
python manage.py makemigrations
python manage.py migrate

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: python manage.py runserver"
echo ""
echo "Default Access:"
echo "  - Application: http://127.0.0.1:8000/"
echo "  - Admin Panel: http://127.0.0.1:8000/admin/"
echo ""
echo "To create a superuser account, run:"
echo "  python manage.py createsuperuser"
echo ""
