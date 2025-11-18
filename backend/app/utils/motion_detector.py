import cv2
import numpy as np
from typing import Optional

class MotionDetector:
    """Detect motion in video frames to trigger OCR processing"""
    
    def __init__(self, threshold: int = 30, min_area: int = 500):
        self.threshold = threshold
        self.min_area = min_area
        self.prev_frame = None
        self.frame_count = 0
        self.motion_detected_count = 0
    
    def detect_motion(self, frame: np.ndarray) -> bool:
        """
        Detect if there's significant motion in the frame
        
        Args:
            frame: Current frame (BGR)
        
        Returns:
            True if motion detected, False otherwise
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            # First frame initialization
            if self.prev_frame is None:
                self.prev_frame = gray
                return True  # Process first frame
            
            # Compute difference
            frame_diff = cv2.absdiff(self.prev_frame, gray)
            thresh = cv2.threshold(frame_diff, self.threshold, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Check for significant motion
            motion_detected = False
            for contour in contours:
                if cv2.contourArea(contour) > self.min_area:
                    motion_detected = True
                    self.motion_detected_count += 1
                    break
            
            # Update previous frame
            self.prev_frame = gray
            self.frame_count += 1
            
            return motion_detected
            
        except Exception as e:
            print(f"Motion detection error: {e}")
            return True  # Process on error to be safe
    
    def reset(self):
        """Reset motion detector"""
        self.prev_frame = None
        self.frame_count = 0
        self.motion_detected_count = 0
    
    def get_stats(self) -> dict:
        """Get motion detection statistics"""
        if self.frame_count == 0:
            return {"motion_ratio": 0, "total_frames": 0, "motion_frames": 0}
        
        return {
            "motion_ratio": self.motion_detected_count / self.frame_count,
            "total_frames": self.frame_count,
            "motion_frames": self.motion_detected_count
        }