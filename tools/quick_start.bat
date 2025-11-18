@echo off
echo ===================================================
echo EvoPlate Enterprise - Quick Start
echo ===================================================
echo.

REM Navigate to project root
cd /d "%~dp0.."

REM Check venv
if not exist "backend\venv" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup_install.bat first.
    pause
    exit /b 1
)

echo [1/3] Starting backend...
start "EvoPlate Backend" cmd /k "cd /d %~dp0..\backend && call venv\Scripts\activate.bat && python run_simple.py"
timeout /t 5 >nul

echo [2/3] Starting frontend...
start "EvoPlate Frontend" cmd /k "cd /d %~dp0..\frontend && yarn start"
timeout /t 8 >nul

echo [3/3] Opening browser...
start http://localhost:3000

echo.
echo ===================================================
echo EvoPlate system started!
echo ===================================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo To stop, close the terminal windows.
echo.
pause
