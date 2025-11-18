import cv2
import numpy as np
from typing import Optional, Tuple, List
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

class YOLOEngine:
    """YOLO-based plate detection and recognition"""
    
    def __init__(self, model_path: Optional[str] = None):
        if not YOLO_AVAILABLE:
            print("YOLO not available. Install ultralytics.")
            self.initialized = False
            return
        
        try:
            # Use YOLOv8 nano model for plate detection
            # In production, use a custom trained model
            self.model = YOLO('yolov8n.pt') if not model_path else YOLO(model_path)
            self.initialized = True
        except Exception as e:
            print(f"YOLO initialization error: {e}")
            self.initialized = False
    
    def detect_plates(self, image: np.ndarray) -> List[dict]:
        """
        Detect license plates in image
        
        Args:
            image: Input image (BGR)
        
        Returns:
            List of detected plates with bounding boxes and confidence
        """
        if not self.initialized:
            return []
        
        try:
            results = self.model(image, verbose=False)
            
            plates = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf[0])
                    
                    plates.append({
                        "bbox": (int(x1), int(y1), int(x2), int(y2)),
                        "confidence": confidence
                    })
            
            return plates
            
        except Exception as e:
            print(f"YOLO detection error: {e}")
            return []
    
    def recognize_plate(self, image: np.ndarray) -> Tuple[Optional[str], float]:
        """
        Detect and extract plate region
        Note: YOLO is primarily for detection, not text recognition
        This returns the cropped plate image for further OCR processing
        
        Args:
            image: Input image (BGR)
        
        Returns:
            (None, confidence) - Returns confidence of detection
        """
        if not self.initialized:
            return None, 0.0
        
        try:
            plates = self.detect_plates(image)
            
            if not plates:
                return None, 0.0
            
            # Get the plate with highest confidence
            best_plate = max(plates, key=lambda x: x['confidence'])
            
            # For YOLO, we just return the confidence
            # The actual plate region can be extracted using bbox
            return None, best_plate['confidence']
            
        except Exception as e:
            print(f"YOLO recognition error: {e}")
            return None, 0.0
    
    def extract_plate_region(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract the plate region from image
        
        Args:
            image: Input image (BGR)
        
        Returns:
            Cropped plate image or None
        """
        plates = self.detect_plates(image)
        
        if not plates:
            return None
        
        # Get the plate with highest confidence
        best_plate = max(plates, key=lambda x: x['confidence'])
        x1, y1, x2, y2 = best_plate['bbox']
        
        # Crop the plate region
        plate_img = image[y1:y2, x1:x2]
        return plate_img
    
    def get_engine_name(self) -> str:
        return "YOLO"