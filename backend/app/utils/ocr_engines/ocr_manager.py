import cv2
import numpy as np
from typing import Optional, Tuple, Literal
from .paddle_engine import PaddleEngine
from .easyocr_engine import EasyOCREngine
from .tesseract_engine import TesseractEngine
from .yolo_engine import YOLOEngine
from .hybrid_engine import HybridEngine

OCREngineType = Literal["paddle", "easy", "tesseract", "yolo", "hybrid"]

class OCRManager:
    """Manage OCR engines and switch between them"""
    
    def __init__(self, default_engine: OCREngineType = "hybrid"):
        self.current_engine = default_engine
        self.engines = {}
        
        # Initialize engines lazily
        self._initialize_engine(default_engine)
    
    def _initialize_engine(self, engine_type: OCREngineType):
        """Initialize a specific engine"""
        if engine_type in self.engines:
            return
        
        try:
            if engine_type == "paddle":
                self.engines[engine_type] = PaddleEngine()
            elif engine_type == "easy":
                self.engines[engine_type] = EasyOCREngine()
            elif engine_type == "tesseract":
                self.engines[engine_type] = TesseractEngine()
            elif engine_type == "yolo":
                self.engines[engine_type] = YOLOEngine()
            elif engine_type == "hybrid":
                self.engines[engine_type] = HybridEngine()
        except Exception as e:
            print(f"Failed to initialize {engine_type}: {e}")
    
    def set_engine(self, engine_type: OCREngineType) -> bool:
        """
        Switch to a different OCR engine
        
        Args:
            engine_type: Engine to switch to
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self._initialize_engine(engine_type)
            
            if engine_type in self.engines and self.engines[engine_type].initialized:
                self.current_engine = engine_type
                print(f"Switched to {engine_type} engine")
                return True
            else:
                print(f"Engine {engine_type} not available")
                return False
        except Exception as e:
            print(f"Failed to switch engine: {e}")
            return False
    
    def recognize_plate(self, image: np.ndarray) -> Tuple[Optional[str], float, str]:
        """
        Recognize plate using current engine
        
        Args:
            image: Input image (BGR)
        
        Returns:
            (plate_text, confidence, engine_name)
        """
        engine = self.engines.get(self.current_engine)
        
        if not engine or not engine.initialized:
            return None, 0.0, "none"
        
        try:
            if self.current_engine == "hybrid":
                return engine.recognize_plate(image)
            else:
                plate_text, confidence = engine.recognize_plate(image)
                return plate_text, confidence, self.current_engine
        except Exception as e:
            print(f"Recognition error: {e}")
            return None, 0.0, "error"
    
    def get_current_engine(self) -> str:
        """Get current engine name"""
        return self.current_engine
    
    def get_available_engines(self) -> list:
        """Get list of available engines"""
        available = []
        for engine_type in ["paddle", "easy", "tesseract", "yolo", "hybrid"]:
            self._initialize_engine(engine_type)
            if engine_type in self.engines and self.engines[engine_type].initialized:
                available.append(engine_type)
        return available

# Global OCR manager instance
ocr_manager = OCRManager()