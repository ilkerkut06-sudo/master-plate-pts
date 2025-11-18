import cv2
import numpy as np
import asyncio
import time
from typing import Optional, Dict
import threading
from queue import Queue, Empty

class LiveVideoPipeline:
    """Pipeline A: Low-res live streaming - NEVER FREEZES"""
    
    def __init__(self, camera_id: str, stream_source: str, fps: int = 15):
        self.camera_id = camera_id
        self.stream_source = stream_source
        self.target_fps = fps
        self.is_running = False
        self.cap = None
        self.current_frame = None
        self.frame_count = 0
        self.actual_fps = 0
        self.last_fps_update = time.time()
        self.thread = None
        self.frame_queue = Queue(maxsize=2)  # Small queue to prevent lag
    
    def start(self):
        """Start live streaming pipeline"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._stream_loop, daemon=True)
        self.thread.start()
        print(f"[Pipeline A] Started for camera {self.camera_id}")
    
    def stop(self):
        """Stop live streaming pipeline"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
        if self.cap:
            self.cap.release()
        print(f"[Pipeline A] Stopped for camera {self.camera_id}")
    
    def _stream_loop(self):
        """Main streaming loop - runs in separate thread"""
        try:
            # Open video capture
            if self.stream_source.isdigit():
                # Webcam
                self.cap = cv2.VideoCapture(int(self.stream_source))
            else:
                # RTSP/ONVIF
                self.cap = cv2.VideoCapture(self.stream_source)
            
            if not self.cap.isOpened():
                print(f"[Pipeline A] Failed to open stream: {self.stream_source}")
                return
            
            # Set low resolution for fast streaming
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, self.target_fps)
            
            frame_delay = 1.0 / self.target_fps
            fps_counter = 0
            fps_start_time = time.time()
            
            while self.is_running:
                start_time = time.time()
                
                ret, frame = self.cap.read()
                
                if not ret:
                    print(f"[Pipeline A] Failed to read frame from {self.camera_id}")
                    time.sleep(1)  # Wait before retry
                    continue
                
                # Resize to even smaller for web streaming
                frame = cv2.resize(frame, (480, 360), interpolation=cv2.INTER_LINEAR)
                
                # Update current frame
                self.current_frame = frame.copy()
                self.frame_count += 1
                
                # Put frame in queue (non-blocking)
                if not self.frame_queue.full():
                    self.frame_queue.put(frame)
                
                # Calculate FPS
                fps_counter += 1
                if time.time() - fps_start_time >= 1.0:
                    self.actual_fps = fps_counter
                    fps_counter = 0
                    fps_start_time = time.time()
                
                # Frame rate limiting
                elapsed = time.time() - start_time
                sleep_time = max(0, frame_delay - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
        
        except Exception as e:
            print(f"[Pipeline A] Error: {e}")
        finally:
            if self.cap:
                self.cap.release()
    
    def get_frame(self) -> Optional[np.ndarray]:
        """Get current frame (non-blocking)"""
        return self.current_frame
    
    def get_frame_jpeg(self) -> Optional[bytes]:
        """Get current frame as JPEG bytes for streaming"""
        if self.current_frame is None:
            return None
        
        try:
            # Encode to JPEG with low quality for fast streaming
            ret, buffer = cv2.imencode('.jpg', self.current_frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
            if ret:
                return buffer.tobytes()
        except Exception as e:
            print(f"[Pipeline A] JPEG encoding error: {e}")
        
        return None
    
    def get_stats(self) -> Dict:
        """Get pipeline statistics"""
        return {
            "camera_id": self.camera_id,
            "pipeline": "A",
            "fps": self.actual_fps,
            "frame_count": self.frame_count,
            "is_running": self.is_running
        }