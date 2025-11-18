"""Web-only version - No OCR, just UI and API"""
import uvicorn
from simple_server import app

print("="*60)
print("EvoPlate Enterprise - Web Interface")
print("="*60)
print()
print("Starting web-only version (no OCR processing)")
print("This version works without Visual C++ Build Tools!")
print()
print("Backend will start on: http://localhost:8000")
print("Frontend will start on: http://localhost:3000")
print()
print("-" * 60)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
