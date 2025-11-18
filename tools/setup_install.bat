@echo off
echo ===================================================
echo EvoPlate Enterprise Edition - Setup
echo ===================================================
echo.

REM Check Python
echo [1/10] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Install Python 3.9+: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Check Node.js
echo [2/10] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found!
    echo Install Node.js 16+: https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js found
echo.

REM Check MongoDB
echo [3/10] Checking MongoDB...
echo [WARNING] MongoDB must be installed and running!
echo MongoDB Community: https://www.mongodb.com/try/download/community
echo After installation, start service: net start MongoDB
pause
echo.

REM Navigate to project root
cd /d "%~dp0.."

REM Create backend venv
echo [4/10] Creating Python virtual environment...
cd backend
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo [OK] Virtual environment created
)
echo.

REM Install Python packages
echo [5/10] Installing Python packages (this may take several minutes)...
call venv\Scripts\activate.bat
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install Python packages!
    pause
    exit /b 1
)
echo [OK] Python packages installed
echo.

REM Check Tesseract
echo [6/10] Checking Tesseract OCR...
where tesseract >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Tesseract OCR not found!
    echo Install manually: https://github.com/UB-Mannheim/tesseract/wiki
    echo Or continue without it (other OCR engines available)
    pause
)
echo.

REM Install frontend packages
echo [7/10] Installing frontend packages...
cd ..\frontend
call yarn install --silent
if errorlevel 1 (
    echo [ERROR] Failed to install frontend packages!
    pause
    exit /b 1
)
echo [OK] Frontend packages installed
echo.

REM Create logs directory
echo [8/10] Creating log directories...
cd ..
mkdir logs 2>nul
echo [OK] Log directories ready
echo.

REM Check FFmpeg
echo [9/10] Checking FFmpeg...
where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo [WARNING] FFmpeg not found!
    echo Install manually: https://www.gyan.dev/ffmpeg/builds/
    echo Video streaming may be limited without it
    pause
)
echo.

echo [10/10] Starting system...
echo.
echo ===================================================
echo Setup Complete!
echo ===================================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Starting servers...
timeout /t 3 >nul

REM Start backend
echo Starting backend...
start "EvoPlate Backend" cmd /k "cd /d %~dp0..\backend && call venv\Scripts\activate.bat && python run.py"
timeout /t 5 >nul

REM Start frontend
echo Starting frontend...
start "EvoPlate Frontend" cmd /k "cd /d %~dp0..\frontend && yarn start"
timeout /t 8 >nul

REM Open browser
echo Opening browser...
start http://localhost:3000

echo.
echo System started!
echo Backend and Frontend terminals are open.
echo Browser opened: http://localhost:3000
echo.
echo To stop the system, close the terminal windows.
pause
