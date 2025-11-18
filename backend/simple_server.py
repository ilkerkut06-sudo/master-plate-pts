from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="EvoPlate API - Simple Version")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "EvoPlate Enterprise API", "status": "running"}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/cameras")
async def get_cameras():
    return []

@app.get("/api/plates")
async def get_plates():
    return []

@app.get("/api/settings/ocr-engines")
async def get_ocr_engines():
    return {
        "available_engines": ["tesseract", "yolo"],
        "current_engine": "tesseract",
        "engines": [
            {"id": "paddle", "name": "PaddleOCR", "description": "Fast and accurate"},
            {"id": "easy", "name": "EasyOCR", "description": "Turkish support"},
            {"id": "tesseract", "name": "Tesseract", "description": "Open source"},
            {"id": "yolo", "name": "YOLO", "description": "Detection only"},
            {"id": "hybrid", "name": "Hybrid", "description": "Best result"}
        ]
    }

@app.get("/api/settings/system-info")
async def get_system_info():
    return {
        "name": "EvoPlate Enterprise Edition",
        "version": "1.0.0",
        "active_cameras": 0,
        "ocr_engine": "tesseract"
    }

@app.get("/api/plates/stats/summary")
async def get_plate_stats():
    return {
        "total_plates": 0,
        "today_plates": 0
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
