import uvicorn
import sys
import os

print("="*50)
print("EvoPlate Enterprise - Starting Backend")
print("="*50)
print()

try:
    # Try to import the full application
    from app.main import app
    print("[OK] Full application loaded")
    print("Note: OCR engines may take time to initialize")
    print()
    
    if __name__ == "__main__":
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
except ImportError as e:
    print(f"[WARNING] Could not load full application: {e}")
    print("Starting simple server instead...")
    print()
    
    # Fallback to simple server
    from simple_server import app
    
    if __name__ == "__main__":
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
