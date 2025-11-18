@echo off
echo ===================================================
echo EvoPlate Enterprise - Web Interface Setup
echo ===================================================
echo.
echo This version does NOT require:
echo - Visual C++ Build Tools
echo - OCR engines
echo - Heavy dependencies
echo.
echo You only need: Python 3.9+, Node.js 16+, MongoDB
echo.
pause

REM Check Python
echo [1/8] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Install: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Check Node.js
echo [2/8] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found!
    echo Install: https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js found
echo.

REM MongoDB check
echo [3/8] MongoDB check...
echo Make sure MongoDB is installed and running:
echo    net start MongoDB
pause
echo.

REM Navigate to project
cd /d "%~dp0.."

REM Create venv
echo [4/8] Creating virtual environment...
cd backend
if exist venv (
    echo Already exists, skipping...
) else (
    python -m venv venv
    echo [OK] Created
)
echo.

REM Install packages
echo [5/8] Installing web packages (fast, no compilation!)...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip wheel
pip install -r requirements_web_only.txt
if errorlevel 1 (
    echo [ERROR] Installation failed!
    pause
    exit /b 1
)
echo [OK] Packages installed
echo.

REM Frontend packages
echo [6/8] Installing frontend packages...
cd ..\frontend
call yarn install
if errorlevel 1 (
    echo [ERROR] Frontend installation failed!
    pause
    exit /b 1
)
echo [OK] Frontend ready
echo.

REM Create logs
echo [7/8] Creating directories...
cd ..
mkdir logs 2>nul
echo [OK] Ready
echo.

echo [8/8] Starting system...
echo.
echo ===================================================
echo Setup Complete! Starting servers...
echo ===================================================
echo.
timeout /t 2 >nul

REM Start backend
echo Starting backend (web-only)...
start "EvoPlate Backend" cmd /k "cd /d %~dp0..\backend && call venv\Scripts\activate.bat && python run_web.py"
timeout /t 4 >nul

REM Start frontend
echo Starting frontend...
start "EvoPlate Frontend" cmd /k "cd /d %~dp0..\frontend && yarn start"
timeout /t 8 >nul

REM Open browser
echo Opening browser...
start http://localhost:3000

echo.
echo ===================================================
echo System Started!
echo ===================================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo.
echo NOTE: This is the WEB INTERFACE version.
echo OCR processing is not included.
echo UI and all pages are fully functional.
echo.
echo To stop: Close the terminal windows
echo.
pause
