import cv2
import numpy as np
import time
from typing import Optional, Dict, Callable
import threading
from queue import Queue
from .motion_detector import MotionDetector
from .roi_extractor import ROIExtractor
from .ocr_engines.ocr_manager import OCRManager
from app.utils.plate_formatter import PlateFormatter

class OCRVideoPipeline:
    """Pipeline B: Full-res OCR processing - INDEPENDENT from Pipeline A"""
    
    def __init__(self, camera_id: str, stream_source: str, 
                 ocr_fps: int = 2, 
                 enable_motion_detection: bool = True,
                 enable_roi: bool = True,
                 roi_coords: Optional[dict] = None,
                 ocr_callback: Optional[Callable] = None):
        
        self.camera_id = camera_id
        self.stream_source = stream_source
        self.ocr_fps = ocr_fps
        self.enable_motion_detection = enable_motion_detection
        self.enable_roi = enable_roi
        self.roi_coords = roi_coords
        self.ocr_callback = ocr_callback
        
        self.is_running = False
        self.cap = None
        self.thread = None
        
        # OCR components
        self.ocr_manager = OCRManager()
        self.motion_detector = MotionDetector() if enable_motion_detection else None
        
        # Statistics
        self.processed_frames = 0
        self.detected_plates = 0
        self.last_detection = None
        self.last_detection_time = None
    
    def start(self):
        """Start OCR pipeline"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._ocr_loop, daemon=True)
        self.thread.start()
        print(f"[Pipeline B] Started for camera {self.camera_id}")
    
    def stop(self):
        """Stop OCR pipeline"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
        if self.cap:
            self.cap.release()
        print(f"[Pipeline B] Stopped for camera {self.camera_id}")
    
    def _ocr_loop(self):
        """Main OCR processing loop - runs independently"""
        try:
            # Open video capture (separate from Pipeline A)
            if self.stream_source.isdigit():
                self.cap = cv2.VideoCapture(int(self.stream_source))
            else:
                self.cap = cv2.VideoCapture(self.stream_source)
            
            if not self.cap.isOpened():
                print(f"[Pipeline B] Failed to open stream: {self.stream_source}")
                return
            
            # Set full resolution for better OCR
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            
            frame_delay = 1.0 / self.ocr_fps
            
            while self.is_running:
                start_time = time.time()
                
                ret, frame = self.cap.read()
                
                if not ret:
                    print(f"[Pipeline B] Failed to read frame from {self.camera_id}")
                    time.sleep(1)
                    continue
                
                # Motion detection (skip OCR if no motion)
                if self.enable_motion_detection and self.motion_detector:
                    has_motion = self.motion_detector.detect_motion(frame)
                    if not has_motion:
                        # No motion, skip OCR processing
                        time.sleep(frame_delay)
                        continue
                
                # Extract ROI if enabled
                process_frame = frame
                if self.enable_roi and self.roi_coords:
                    process_frame = ROIExtractor.extract_roi(frame, self.roi_coords)
                
                # Run OCR
                plate_text, confidence, engine = self.ocr_manager.recognize_plate(process_frame)
                
                self.processed_frames += 1
                
                # If plate detected with sufficient confidence
                if plate_text and confidence > 0.6:
                    # Validate plate format
                    if PlateFormatter.validate_plate(plate_text):
                        formatted_plate = PlateFormatter.format_plate(plate_text)
                        
                        # Check if this is a new detection (debounce)
                        is_new_detection = True
                        if self.last_detection == formatted_plate:
                            if self.last_detection_time and (time.time() - self.last_detection_time) < 5:
                                is_new_detection = False
                        
                        if is_new_detection:
                            self.detected_plates += 1
                            self.last_detection = formatted_plate
                            self.last_detection_time = time.time()
                            
                            # Callback with detection result
                            if self.ocr_callback:
                                try:
                                    self.ocr_callback({
                                        "camera_id": self.camera_id,
                                        "plate": formatted_plate,
                                        "confidence": confidence,
                                        "engine": engine,
                                        "timestamp": time.time()
                                    })
                                except Exception as e:
                                    print(f"[Pipeline B] Callback error: {e}")
                            
                            print(f"[Pipeline B] Detected: {formatted_plate} (conf: {confidence:.2f}, engine: {engine})")
                
                # Frame rate limiting
                elapsed = time.time() - start_time
                sleep_time = max(0, frame_delay - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
        
        except Exception as e:
            print(f"[Pipeline B] Error: {e}")
        finally:
            if self.cap:
                self.cap.release()
    
    def set_ocr_engine(self, engine: str) -> bool:
        """Change OCR engine"""
        return self.ocr_manager.set_engine(engine)
    
    def get_stats(self) -> Dict:
        """Get pipeline statistics"""
        return {
            "camera_id": self.camera_id,
            "pipeline": "B",
            "processed_frames": self.processed_frames,
            "detected_plates": self.detected_plates,
            "last_detection": self.last_detection,
            "current_engine": self.ocr_manager.get_current_engine(),
            "is_running": self.is_running
        }