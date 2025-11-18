import cv2
import numpy as np
from typing import Optional, Tuple, List, Dict
from .paddle_engine import PaddleEngine
from .easyocr_engine import EasyOCREngine
from .tesseract_engine import TesseractEngine
from .yolo_engine import YOLOEngine
from app.utils.plate_formatter import PlateFormatter

class HybridEngine:
    """Hybrid OCR engine that combines multiple engines and selects the best result"""
    
    def __init__(self):
        print("Initializing Hybrid OCR Engine...")
        
        # Initialize all engines
        self.engines = {}
        
        # PaddleOCR
        try:
            paddle = PaddleEngine()
            if paddle.initialized:
                self.engines['paddle'] = paddle
                print("✓ PaddleOCR loaded")
        except Exception as e:
            print(f"✗ PaddleOCR failed: {e}")
        
        # EasyOCR
        try:
            easy = EasyOCREngine()
            if easy.initialized:
                self.engines['easy'] = easy
                print("✓ EasyOCR loaded")
        except Exception as e:
            print(f"✗ EasyOCR failed: {e}")
        
        # Tesseract
        try:
            tess = TesseractEngine()
            if tess.initialized:
                self.engines['tesseract'] = tess
                print("✓ Tesseract loaded")
        except Exception as e:
            print(f"✗ Tesseract failed: {e}")
        
        # YOLO (for detection only)
        try:
            yolo = YOLOEngine()
            if yolo.initialized:
                self.engines['yolo'] = yolo
                print("✓ YOLO loaded")
        except Exception as e:
            print(f"✗ YOLO failed: {e}")
        
        self.initialized = len(self.engines) > 0
        print(f"Hybrid Engine initialized with {len(self.engines)} engines")
    
    def recognize_plate(self, image: np.ndarray, use_yolo_detection: bool = True) -> Tuple[Optional[str], float, str]:
        """
        Recognize plate using all engines and return the best result
        
        Args:
            image: Input image (BGR)
            use_yolo_detection: Whether to use YOLO for plate detection first
        
        Returns:
            (plate_text, confidence, engine_name)
        """
        if not self.initialized:
            return None, 0.0, "none"
        
        # Step 1: Use YOLO to detect and extract plate region (if available)
        process_image = image
        if use_yolo_detection and 'yolo' in self.engines:
            plate_region = self.engines['yolo'].extract_plate_region(image)
            if plate_region is not None:
                process_image = plate_region
        
        # Step 2: Run all OCR engines in parallel
        results = []
        
        for engine_name, engine in self.engines.items():
            if engine_name == 'yolo':  # Skip YOLO for text recognition
                continue
            
            try:
                plate_text, confidence = engine.recognize_plate(process_image)
                
                if plate_text and len(plate_text) >= 5:  # Minimum plate length
                    # Validate and format plate
                    if PlateFormatter.validate_plate(plate_text):
                        formatted_plate = PlateFormatter.format_plate(plate_text)
                        results.append({
                            'text': formatted_plate,
                            'confidence': confidence,
                            'engine': engine_name
                        })
            except Exception as e:
                print(f"Error in {engine_name}: {e}")
        
        if not results:
            return None, 0.0, "none"
        
        # Step 3: Select best result based on confidence and validation
        best_result = max(results, key=lambda x: x['confidence'])
        
        return best_result['text'], best_result['confidence'], best_result['engine']
    
    def get_available_engines(self) -> List[str]:
        """Get list of available OCR engines"""
        return list(self.engines.keys())
    
    def get_engine_name(self) -> str:
        return "Hybrid (" + ", ".join(self.get_available_engines()) + ")"