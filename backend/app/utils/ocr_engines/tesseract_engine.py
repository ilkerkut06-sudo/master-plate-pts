import cv2
import numpy as np
from typing import Optional, Tuple
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

class TesseractEngine:
    """Tesseract OCR engine for Turkish plate recognition"""
    
    def __init__(self):
        if not TESSERACT_AVAILABLE:
            print("Tesseract not available. Install pytesseract.")
            self.initialized = False
            return
        
        try:
            # Test Tesseract installation
            pytesseract.get_tesseract_version()
            self.initialized = True
        except Exception as e:
            print(f"Tesseract initialization error: {e}")
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
            
            # Run OCR with Turkish config
            custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            data = pytesseract.image_to_data(processed, lang='tur+eng', config=custom_config, output_type=pytesseract.Output.DICT)
            
            # Extract text and confidence
            texts = []
            confidences = []
            
            for i, conf in enumerate(data['conf']):
                if int(conf) > 0:
                    text = data['text'][i]
                    if text.strip():
                        texts.append(text)
                        confidences.append(int(conf))
            
            if not texts:
                return None, 0.0
            
            # Combine texts
            plate_text = ''.join(texts).upper()
            avg_confidence = sum(confidences) / len(confidences) / 100.0  # Normalize to 0-1
            
            # Filter Turkish plate characters
            plate_text = self._filter_plate_chars(plate_text)
            
            return plate_text, avg_confidence
            
        except Exception as e:
            print(f"Tesseract recognition error: {e}")
            return None, 0.0
    
    def _preprocess(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR"""
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Resize for better recognition
        scale_factor = 2
        width = int(gray.shape[1] * scale_factor)
        height = int(gray.shape[0] * scale_factor)
        gray = cv2.resize(gray, (width, height), interpolation=cv2.INTER_CUBIC)
        
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
        filtered = re.sub(r'[^A-Z0-9]', '', text)
        return filtered
    
    def get_engine_name(self) -> str:
        return "Tesseract"