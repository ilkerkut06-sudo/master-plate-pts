import cv2
import numpy as np
from typing import Optional, Tuple
import easyocr

class EasyOCREngine:
    """EasyOCR engine for Turkish plate recognition"""
    
    def __init__(self):
        try:
            # Initialize with Turkish and English
            self.reader = easyocr.Reader(['tr', 'en'], gpu=False, verbose=False)
            self.initialized = True
        except Exception as e:
            print(f"EasyOCR initialization error: {e}")
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
            results = self.reader.readtext(processed)
            
            if not results:
                return None, 0.0
            
            # Extract text and confidence
            texts = []
            confidences = []
            
            for (bbox, text, conf) in results:
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
            print(f"EasyOCR recognition error: {e}")
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
        
        # Adaptive threshold
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, 11, 2)
        
        return binary
    
    def _filter_plate_chars(self, text: str) -> str:
        """Filter only valid Turkish plate characters"""
        import re
        filtered = re.sub(r'[^A-Z0-9]', '', text)
        return filtered
    
    def get_engine_name(self) -> str:
        return "EasyOCR"