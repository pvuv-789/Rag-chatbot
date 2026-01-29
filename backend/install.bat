@echo off
echo ============================================
echo RAG Chatbot Backend - Installation Script
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or 3.12 from python.org
    pause
    exit /b 1
)

echo Detected Python version:
python --version
echo.

REM Check if virtual environment exists
if exist "venv\" (
    echo Virtual environment already exists.
    set /p recreate="Do you want to recreate it? (y/n): "
    if /i "%recreate%"=="y" (
        echo Removing old virtual environment...
        rmdir /s /q venv
    )
)

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
echo.

pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ============================================
    echo ERROR: Failed to install dependencies
    echo ============================================
    echo.
    echo If you're using Python 3.13, please see:
    echo PYTHON_313_COMPATIBILITY.md
    echo.
    echo Recommended: Use Python 3.11 or 3.12
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo Installation completed!
echo ============================================
echo.

REM Test imports
echo Testing package imports...
python test_imports.py
echo.

REM Check for .env file
if not exist ".env" (
    echo ============================================
    echo IMPORTANT: Setup .env file
    echo ============================================
    echo.
    echo .env file not found. Please:
    echo 1. Copy .env.example to .env
    echo 2. Add your GEMINI_API_KEY
    echo.
    echo Command: copy .env.example .env
    echo.
)

echo ============================================
echo Next Steps:
echo ============================================
echo 1. Make sure .env file exists with your API key
echo 2. Run: uvicorn main:app --reload
echo 3. Open: http://localhost:8000/docs
echo ============================================
echo.

pause
