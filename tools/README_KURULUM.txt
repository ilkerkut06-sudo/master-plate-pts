===================================================
EvoPlate Enterprise Edition - Kurulum Kılavuzu
===================================================

## ÖN GEREKSİNİMLER

1. Python 3.9 veya üzeri
   İndir: https://www.python.org/downloads/
   NOT: Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin!

2. Node.js 16 veya üzeri
   İndir: https://nodejs.org/

3. MongoDB Community Edition
   İndir: https://www.mongodb.com/try/download/community
   Kurulum sonrası servisi başlatın:
   > net start MongoDB

4. Tesseract OCR (Opsiyonel)
   İndir: https://github.com/UB-Mannheim/tesseract/wiki
   NOT: PATH'e eklemeyi unutmayın

5. FFmpeg (Opsiyonel ama önerilen)
   İndir: https://www.gyan.dev/ffmpeg/builds/
   NOT: PATH'e eklemeyi unutmayın

---

## KURULUM ADIMLARI

### İlk Kurulum (Sadece bir kez):

1. Tüm ön gereksinimleri yükleyin
2. MongoDB servisini başlatın
3. "setup_start.bat" dosyasını çift tıklayarak çalıştırın
4. Script otomatik olarak:
   - Python virtual environment oluşturacak
   - Tüm bağımlılıkları yükleyecek
   - Backend ve Frontend'i başlatacak
   - Tarayıcıyı otomatik açacak

### Sonraki Kullanımlar:

1. MongoDB servisinin çalıştığından emin olun
2. "start_server.bat" dosyasını çift tıklayarak çalıştırın
3. Sistem otomatik başlayacak ve tarayıcı açılacak

---

## SİSTEM KULLANIMI

Backend: http://localhost:8000
Frontend: http://localhost:3000
API Dokümantasyonu: http://localhost:8000/docs

### İlk Kamera Ekleme:

1. Dashboard'da "Kameralar" menüsüne gidin
2. "Yeni Kamera" butonuna tıklayın
3. Kamera tipini seçin:
   - RTSP: IP kamera için (rtsp://username:password@ip:port/stream)
   - ONVIF: ONVIF destekli kamera için
   - Webcam: Bilgisayara bağlı webcam (index: 0, 1, 2...)
4. "Kaydet" butonuna tıklayın
5. Dashboard'a dönüp kamerayı başlatın

### OCR Motor Seçimi:

1. "Ayarlar" menüsüne gidin
2. "OCR Motor Seçimi" bölümünden motor seçin:
   - PaddleOCR: Hızlı ve doğru
   - EasyOCR: Türkçe karakter desteği
   - Tesseract: Açık kaynak
   - YOLO: Sadece plaka tespiti
   - Hybrid: En iyi sonuç (önerilen)

---

## SİSTEMİ DURDURMA

Backend ve Frontend terminal pencerelerini kapatın veya CTRL+C ile durdurun.

---

## SORUN GİDERME

### MongoDB bağlantı hatası:
- MongoDB servisinin çalıştığından emin olun: net start MongoDB
- MongoDB varsayılan port'ta (27017) çalışmalı

### Kamera bağlanamıyor:
- RTSP URL'nin doğru olduğundan emin olun
- Webcam index doğru mu kontrol edin (genellikle 0)
- Firewall kamera bağlantısını engelliyor olabilir

### OCR çalışmıyor:
- En az bir OCR motoru kurulu olmalı (PaddleOCR ve EasyOCR otomatik yüklenir)
- Tesseract kullanıyorsanız PATH'e eklendiğinden emin olun
- "Hybrid" modu kullanın, otomatik en iyi motoru seçer

### Frontend açılmıyor:
- Port 3000 başka bir uygulama tarafından kullanılıyor olabilir
- Terminal'de hata mesajlarını kontrol edin

---

## TEKNİK DETAYLAR

### Dual Pipeline Mimarisi:

- Pipeline A (Live): Düşük çözünürlük, asla donmaz, WebSocket stream
- Pipeline B (OCR): Yüksek çözünürlük, ROI + Motion Detection, plaka tanıma

### Hybrid OCR:

Tüm OCR motorları paralel çalışır:
- PaddleOCR
- EasyOCR  
- Tesseract
- YOLO (plaka tespiti)

En yüksek confidence skoru olan sonuç seçilir.

### Optimizasyonlar:

- ROI (Region of Interest): Sadece plaka bölgesi işlenir
- Motion Detection: Hareket yoksa OCR çalışmaz (CPU tasarrufu)
- WebSocket: Gerçek zamanlı stream ve event'ler

---

## DESTEK

Sorun yaşarsanız:
1. logs/ klasöründeki log dosyalarını kontrol edin
2. Terminal pencerelerindeki hata mesajlarına bakın
3. MongoDB, Python, Node.js versiyonlarını kontrol edin

===================================================
İyi kullanımlar!
===================================================