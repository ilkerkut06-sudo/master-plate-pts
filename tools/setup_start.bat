@echo off
chcp 65001 >nul
echo ===================================================
echo EvoPlate Enterprise Edition - Otomatik Kurulum
echo ===================================================
echo.

REM Check if Python is installed
echo [1/10] Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadi!
    echo Python 3.9+ yukleyin: https://www.python.org/downloads/
    echo Kurulum sirasinda "Add Python to PATH" secenegini isaretleyin!
    pause
    exit /b 1
)
echo [OK] Python bulundu
echo.

REM Check if Node.js is installed
echo [2/10] Node.js kontrol ediliyor...
node --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Node.js bulunamadi!
    echo Node.js 16+ yukleyin: https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js bulundu
echo.

REM Check if MongoDB is running
echo [3/10] MongoDB kontrol ediliyor...
echo [UYARI] MongoDB kurulu ve calisir durumda olmalidir!
echo MongoDB Community Edition: https://www.mongodb.com/try/download/community
echo MongoDB kurulumu sonrasi servisi baslatin: "net start MongoDB"
pause
echo.

REM Navigate to project root
cd /d "%~dp0.."

REM Create backend virtual environment
echo [4/10] Python sanal ortami olusturuluyor...
cd backend
if exist venv (
    echo Virtual environment zaten mevcut, atlaniyor...
) else (
    python -m venv venv
    echo [OK] Virtual environment olusturuldu
)
echo.

REM Activate virtual environment and install dependencies
echo [5/10] Python kutuphaneleri yukleniyor (bu birkaç dakika surebilir)...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [HATA] Python kutuphaneleri yuklenemedi!
    pause
    exit /b 1
)
echo [OK] Python kutuphaneleri yuklendi
echo.

REM Install Tesseract OCR
echo [6/10] Tesseract OCR kontrol ediliyor...
where tesseract >nul 2>&1
if errorlevel 1 (
    echo [UYARI] Tesseract OCR bulunamadi!
    echo Manuel yukleyin: https://github.com/UB-Mannheim/tesseract/wiki
    echo Kurulum sonrasi PATH'e ekleyin veya Tesseract olmadan devam edebilirsiniz
    echo (Diger OCR motorlari kullanilabilir)
    pause
)
echo.

REM Install frontend dependencies
echo [7/10] Frontend kutuphaneleri yukleniyor...
cd ..\frontend
call yarn install
if errorlevel 1 (
    echo [HATA] Frontend kutuphaneleri yuklenemedi!
    pause
    exit /b 1
)
echo [OK] Frontend kutuphaneleri yuklendi
echo.

REM Create logs directory
echo [8/10] Log klasorleri olusturuluyor...
cd ..
mkdir logs 2>nul
echo [OK] Log klasorleri hazir
echo.

REM Download ffmpeg (optional but recommended)
echo [9/10] FFmpeg kontrol ediliyor...
where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo [UYARI] FFmpeg bulunamadi!
    echo Manuel yukleyin: https://www.gyan.dev/ffmpeg/builds/
    echo FFmpeg olmadan video stream ozellikleri kisitli olabilir
    pause
)
echo.

echo [10/10] Sistem baslatiiliyor...
echo.
echo ===================================================
echo Kurulum tamamlandi!
echo ===================================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Sistem baslatiliyor...
timeout /t 3 >nul

REM Start backend in new window
echo Backend baslatiiliyor...
start "EvoPlate Backend" cmd /k "cd /d %~dp0..\backend && call venv\Scripts\activate.bat && python run.py"
timeout /t 5 >nul

REM Start frontend in new window
echo Frontend baslatiiliyor...
start "EvoPlate Frontend" cmd /k "cd /d %~dp0..\frontend && yarn start"
timeout /t 8 >nul

REM Open browser
echo Tarayici aciliyor...
start http://localhost:3000

echo.
echo Sistem baslatildi!
echo Backend ve Frontend terminalleri acildi.
echo Tarayici acildi: http://localhost:3000
echo.
echo Sistemi durdurmak icin terminal pencerelerini kapatin.
pause