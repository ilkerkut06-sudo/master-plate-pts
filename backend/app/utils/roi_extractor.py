import cv2
import numpy as np
from typing import Optional, Tuple

class ROIExtractor:
    """Extract Region of Interest for plate detection"""
    
    @staticmethod
    def extract_roi(frame: np.ndarray, roi_coords: Optional[dict] = None) -> np.ndarray:
        """
        Extract ROI from frame
        
        Args:
            frame: Input frame
            roi_coords: {"x1": int, "y1": int, "x2": int, "y2": int} or None for full frame
        
        Returns:
            ROI frame
        """
        if not roi_coords:
            return frame
        
        try:
            x1 = roi_coords.get("x1", 0)
            y1 = roi_coords.get("y1", 0)
            x2 = roi_coords.get("x2", frame.shape[1])
            y2 = roi_coords.get("y2", frame.shape[0])
            
            # Ensure coordinates are within frame bounds
            x1 = max(0, min(x1, frame.shape[1]))
            y1 = max(0, min(y1, frame.shape[0]))
            x2 = max(0, min(x2, frame.shape[1]))
            y2 = max(0, min(y2, frame.shape[0]))
            
            return frame[y1:y2, x1:x2]
        except Exception as e:
            print(f"ROI extraction error: {e}")
            return frame
    
    @staticmethod
    def draw_roi(frame: np.ndarray, roi_coords: Optional[dict] = None, color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
        """
        Draw ROI rectangle on frame for visualization
        """
        if not roi_coords:
            return frame
        
        try:
            x1 = roi_coords.get("x1", 0)
            y1 = roi_coords.get("y1", 0)
            x2 = roi_coords.get("x2", frame.shape[1])
            y2 = roi_coords.get("y2", frame.shape[0])
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, "ROI", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            return frame
        except Exception as e:
            print(f"ROI drawing error: {e}")
            return frame