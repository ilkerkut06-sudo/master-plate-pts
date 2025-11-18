import cv2
import numpy as np
from typing import Optional, Tuple
from paddleocr import PaddleOCR
import os

class PaddleEngine:
    """PaddleOCR engine for Turkish plate recognition"""
    
    def __init__(self):
        try:
            # Suppress PaddlePaddle warnings
            os.environ['FLAGS_allocator_strategy'] = 'auto_growth'
            self.ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, show_log=False)
            self.initialized = True
        except Exception as e:
            print(f"PaddleOCR initialization error: {e}")
            self.initialized = False
    
    def recognize_plate(self, image: np.ndarray) -> Tuple[Optional[str], float]:
        """
        Recognize plate from image
        
        Args:
            image: Input image (BGR)
        
        Returns:
            (plate_text, confidence) or (None, 0.0)
        """
        if not self.initialized:
            return None, 0.0
        
        try:
            # Preprocess image
            processed = self._preprocess(image)
            
            # Run OCR
            result = self.ocr.ocr(processed, cls=True)
            
            if not result or not result[0]:
                return None, 0.0
            
            # Extract text and confidence
            texts = []
            confidences = []
            
            for line in result[0]:
                text = line[1][0]
                conf = line[1][1]
                texts.append(text)
                confidences.append(conf)
            
            if not texts:
                return None, 0.0
            
            # Combine texts
            plate_text = ''.join(texts).upper()
            avg_confidence = sum(confidences) / len(confidences)
            
            # Filter Turkish plate characters
            plate_text = self._filter_plate_chars(plate_text)
            
            return plate_text, avg_confidence
            
        except Exception as e:
            print(f"PaddleOCR recognition error: {e}")
            return None, 0.0
    
    def _preprocess(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR"""
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Increase contrast
        gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=10)
        
        # Denoise
        gray = cv2.fastNlMeansDenoising(gray)
        
        # Threshold
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary
    
    def _filter_plate_chars(self, text: str) -> str:
        """Filter only valid Turkish plate characters"""
        import re
        # Turkish plates: digits and letters (no special chars)
        filtered = re.sub(r'[^A-Z0-9]', '', text)
        return filtered
    
    def get_engine_name(self) -> str:
        return "PaddleOCR"