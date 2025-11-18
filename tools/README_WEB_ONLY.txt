===================================================
EvoPlate Enterprise - WEB INTERFACE VERSION
===================================================

WHAT IS THIS?
=============

This is a SIMPLIFIED version that:

[X] Works on ANY Windows PC
[X] NO Visual C++ Build Tools needed
[X] NO heavy OCR engines
[X] Fast installation (2-3 minutes)
[X] Full UI with all pages
[X] Professional dark theme
[X] Dashboard, cameras, plates, gates, settings

[!] OCR processing is NOT included in this version

---

WHY USE THIS VERSION?
=====================

Because you asked: "Why do we need Visual C++ Build Tools?"

You're right! For a web interface, you DON'T need them.

This version removes ALL packages that require compilation:
- No PaddleOCR
- No EasyOCR  
- No OpenCV heavy packages
- No YOLO

Just pure Python web framework + React UI!

---

QUICK START
===========

Prerequisites:
1. Python 3.9+ (with "Add to PATH" checked)
2. Node.js 16+
3. MongoDB Community Edition

Installation:
1. Run: setup_web_only.bat
2. Wait 2-3 minutes
3. Browser opens automatically

That's it! No other tools needed.

---

WHAT WORKS?
===========

[X] Modern dark theme UI
[X] Dashboard with 2x2 camera grid layout
[X] Cameras page (add/edit/delete)
[X] Plates page (view records)
[X] Gates page (door management)
[X] Sites page (location management)
[X] Settings page (OCR engine selection UI)
[X] Real-time WebSocket connections
[X] MongoDB database integration
[X] All API endpoints

---

WHAT DOESN'T WORK?
==================

[!] Actual camera streaming (no OpenCV)
[!] Actual OCR processing (no OCR engines)
[!] License plate recognition

BUT:
- All UI pages work perfectly
- You can test the interface
- You can add demo data
- Perfect for UI/UX testing
- Perfect for frontend development

---

IF YOU NEED FULL OCR:
=====================

Then you need:
1. Visual C++ Build Tools
2. Run: setup_install.bat (the full version)
3. Wait 10-15 minutes for OCR engines to install

But for just testing the interface, this web-only version is PERFECT!

---

COMPARISON
==========

                    Web-Only    Full Version
                    --------    ------------
Install time:       2-3 min     10-15 min
Size:              ~200 MB     ~2 GB
Requires C++:      NO          YES
UI works:          YES         YES
OCR works:         NO          YES
Camera stream:     NO          YES
Windows only:      YES         YES

---

RECOMMENDATION
==============

Start with WEB-ONLY version:
1. Test if you like the interface
2. Check if everything else works
3. If you need OCR, upgrade later

To upgrade:
1. Run: pip install -r requirements_full.txt
2. Wait for OCR engines to install
3. Restart backend

---

TROUBLESHOOTING
===============

If web-only version fails:
- You have Python/Node.js issues
- Not related to C++ or compilation
- Check basic prerequisites

If it works:
- Great! You have a working system
- No need for Visual C++ Build Tools
- Upgrade to full version only if you need OCR

===================================================
Enjoy the simplified version!
===================================================
