@echo off
REM Setup Virtual Environment Script for Coal Blending Optimizer Backend (Windows)

echo.
echo ========================================
echo Setting up Python Virtual Environment
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Virtual environment created successfully
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

echo Pip upgraded
echo.

REM Install dependencies
echo Installing dependencies from requirements.txt...
echo This may take a few minutes...
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo All dependencies installed successfully
echo.

REM Verify installation
echo Verifying installation...
python -c "import fastapi; import boto3; import pulp; print('Core packages verified')" 2>nul

if errorlevel 1 (
    echo WARNING: Some packages may not be installed correctly
) else (
    echo Installation verified successfully
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the backend server:
echo   1. Make sure virtual environment is activated:
echo      venv\Scripts\activate
echo.
echo   2. Run the server:
echo      python main.py
echo.
echo   3. Server will be available at:
echo      http://127.0.0.1:8000
echo.
echo To deactivate virtual environment later:
echo   deactivate
echo.
echo ========================================

pause
