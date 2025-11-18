# EvoPlate Enterprise Edition

## Türk Plaka Tanıma Sistemi (Turkish License Plate Recognition System)

### Özellikler

✅ **Dual Pipeline Mimarisi**
- Pipeline A: Düşük çözünürlük, donmayan canlı yayın
- Pipeline B: Yüksek çözünürlük, bağımsız OCR işleme

✅ **Hybrid OCR Motoru**
- PaddleOCR
- EasyOCR (Türkçe karakter desteği)
- Tesseract
- YOLOv8 (Plaka tespiti)
- En yüksek güven skoru otomatik seçilir

✅ **Gelişmiş Özellikler**
- ROI (Region of Interest) - Sadece plaka bölgesi işlenir
- Motion Detection - CPU optimizasyonu
- WebSocket - Gerçek zamanlı stream
- RTSP/ONVIF/Webcam desteği

✅ **Profesyonel UI**
- Modern dark tema
- 2x2 kamera grid
- Canlı istatistikler
- Log paneli
- OCR motor seçimi

### Kurulum

#### Öngereksinimler

1. Python 3.9+
2. Node.js 16+
3. MongoDB Community Edition
4. Tesseract OCR (Opsiyonel)
5. FFmpeg (Opsiyonel)

#### Windows Kurulumu (Hızlı Başlangıç)

1. Tüm öngereksinimleri yükleyin
2. MongoDB servisini başlatın: `net start MongoDB`
3. `tools/setup_start.bat` dosyasını çalıştırın
4. İşlem tamamlanınca tarayıcı otomatik açılacak

#### Sonraki Kullanımlar

`tools/start_server.bat` dosyasını çalıştırın

### Manuel Kurulum

#### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python run.py
```

#### Frontend

```bash
cd frontend
yarn install
yarn start
```

### Kullanım

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

#### Kamera Ekleme

1. Dashboard → Kameralar → Yeni Kamera
2. Kamera tipi seçin (RTSP/ONVIF/Webcam)
3. Stream URL veya webcam index girin
4. Kaydet ve başlat

#### OCR Motor Seçimi

1. Ayarlar → OCR Motor Seçimi
2. İstediğiniz motoru seçin (Hybrid önerilir)

### Mimari

```
┌─────────────────────────────────────────────────────────┐
│                  EvoPlate Enterprise                     │
├─────────────────────────────────────────────────────────┤
│  Frontend (React + Tailwind)                            │
│  ├── Dashboard (2x2 Camera Grid)                        │
│  ├── Real-time Stats                                    │
│  ├── Live Logs Panel                                    │
│  └── Settings (OCR Engine Selector)                     │
├─────────────────────────────────────────────────────────┤
│  Backend (FastAPI)                                      │
│  ├── Dual Pipeline System                               │
│  │   ├── Pipeline A: Live Stream (Low-res, No freeze)  │
│  │   └── Pipeline B: OCR Processing (High-res)         │
│  ├── Hybrid OCR Engine                                  │
│  │   ├── PaddleOCR                                      │
│  │   ├── EasyOCR                                        │
│  │   ├── Tesseract                                      │
│  │   └── YOLO                                           │
│  ├── ROI Extraction                                     │
│  ├── Motion Detection                                   │
│  └── WebSocket Manager                                  │
├─────────────────────────────────────────────────────────┤
│  Database (MongoDB)                                     │
│  ├── Cameras                                            │
│  ├── Plates                                             │
│  ├── Gates                                              │
│  ├── Sites                                              │
│  └── Logs                                               │
└─────────────────────────────────────────────────────────┘
```

### Proje Yapısı

```
evoplate/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Konfigürasyon
│   │   ├── database/            # MongoDB bağlantı
│   │   ├── models/              # Veri modelleri
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # İş mantığı
│   │   └── utils/
│   │       ├── ocr_engines/     # OCR motorları
│   │       ├── video_pipeline_live.py    # Pipeline A
│   │       ├── video_pipeline_ocr.py     # Pipeline B
│   │       ├── roi_extractor.py
│   │       └── motion_detector.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/          # UI bileşenleri
│   │   ├── pages/               # Sayfalar
│   │   ├── utils/               # Yardımcı fonksiyonlar
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── tools/
│   ├── setup_start.bat          # İlk kurulum scripti
│   ├── start_server.bat         # Server başlatma scripti
│   └── README_KURULUM.txt       # Kurulum kılavuzu
└── README.md
```

### API Endpoints

#### Cameras
- `GET /api/cameras` - Tüm kameraları listele
- `POST /api/cameras` - Yeni kamera ekle
- `PUT /api/cameras/{id}` - Kamera güncelle
- `DELETE /api/cameras/{id}` - Kamera sil
- `POST /api/cameras/{id}/start` - Kamera başlat
- `POST /api/cameras/{id}/stop` - Kamera durdur
- `WS /api/cameras/ws/{id}` - Canlı stream

#### Plates
- `GET /api/plates` - Tüm plakaları listele
- `GET /api/plates/{id}` - Plaka detayı
- `GET /api/plates/camera/{camera_id}` - Kameraya göre plakalar
- `GET /api/plates/search/{plate_number}` - Plaka ara

#### Gates
- `GET /api/gates` - Tüm kapıları listele
- `POST /api/gates` - Yeni kapı ekle
- `POST /api/gates/{id}/open` - Kapı aç
- `POST /api/gates/{id}/test` - Kapı test

#### Settings
- `GET /api/settings/ocr-engines` - Mevcut OCR motorları
- `POST /api/settings/ocr-engine` - OCR motor değiştir
- `GET /api/settings/system-info` - Sistem bilgisi

### Teknolojiler

**Backend:**
- FastAPI
- Python 3.9+
- Motor (Async MongoDB driver)
- OpenCV
- PaddleOCR
- EasyOCR
- Tesseract
- YOLOv8 (Ultralytics)
- WebSockets

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- Framer Motion
- Axios
- React Router

**Database:**
- MongoDB

### Lisans

EvoPlate Enterprise Edition

### Destek

Sorun yaşarsanız:
1. `logs/` klasöründeki log dosyalarını kontrol edin
2. MongoDB servisinin çalıştığından emin olun
3. Terminal'deki hata mesajlarına bakın

---

**© 2024 EvoPlate Enterprise - Turkish License Plate Recognition System**
