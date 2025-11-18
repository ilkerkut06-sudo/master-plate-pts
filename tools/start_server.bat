@echo off
chcp 65001 >nul
echo ===================================================
echo EvoPlate Enterprise Edition - Server Başlat
echo ===================================================
echo.

REM Navigate to project root
cd /d "%~dp0.."

REM Check if virtual environment exists
if not exist "backend\venv" (
    echo [HATA] Virtual environment bulunamadi!
    echo Lutfen once setup_start.bat calistirin.
    pause
    exit /b 1
)

echo [1/3] Backend baslatiiliyor...
start "EvoPlate Backend" cmd /k "cd /d %~dp0..\backend && call venv\Scripts\activate.bat && python run.py"
timeout /t 5 >nul

echo [2/3] Frontend baslatiiliyor...
start "EvoPlate Frontend" cmd /k "cd /d %~dp0..\frontend && yarn start"
timeout /t 8 >nul

echo [3/3] Tarayici aciliyor...
start http://localhost:3000

echo.
echo ===================================================
echo EvoPlate sistemi baslatildi!
echo ===================================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Sistemi durdurmak icin terminal pencerelerini kapatin.
echo.
pause