from fastapi import WebSocket
from typing import Dict, Set
import asyncio
import json

class WebSocketManager:
    """Manage WebSocket connections for real-time updates"""
    
    def __init__(self):
        # Active connections: {camera_id: Set[WebSocket]}
        self.camera_connections: Dict[str, Set[WebSocket]] = {}
        # General event connections
        self.event_connections: Set[WebSocket] = set()
    
    async def connect_camera(self, websocket: WebSocket, camera_id: str):
        """Connect client to camera stream"""
        await websocket.accept()
        
        if camera_id not in self.camera_connections:
            self.camera_connections[camera_id] = set()
        
        self.camera_connections[camera_id].add(websocket)
        print(f"Client connected to camera {camera_id}. Total: {len(self.camera_connections[camera_id])}")
    
    async def connect_events(self, websocket: WebSocket):
        """Connect client to event stream"""
        await websocket.accept()
        self.event_connections.add(websocket)
        print(f"Client connected to events. Total: {len(self.event_connections)}")
    
    def disconnect_camera(self, websocket: WebSocket, camera_id: str):
        """Disconnect client from camera stream"""
        if camera_id in self.camera_connections:
            self.camera_connections[camera_id].discard(websocket)
            print(f"Client disconnected from camera {camera_id}")
    
    def disconnect_events(self, websocket: WebSocket):
        """Disconnect client from event stream"""
        self.event_connections.discard(websocket)
        print(f"Client disconnected from events")
    
    async def broadcast_camera_frame(self, camera_id: str, frame_data: bytes):
        """Broadcast frame to all clients watching this camera"""
        if camera_id not in self.camera_connections:
            return
        
        disconnected = set()
        
        for connection in self.camera_connections[camera_id]:
            try:
                await connection.send_bytes(frame_data)
            except Exception as e:
                print(f"Error sending frame: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.camera_connections[camera_id].discard(connection)
    
    async def broadcast_event(self, event_type: str, data: dict):
        """Broadcast event to all connected clients"""
        message = json.dumps({
            "type": event_type,
            "data": data
        })
        
        disconnected = set()
        
        for connection in self.event_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending event: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.event_connections.discard(connection)
    
    async def send_to_camera_clients(self, camera_id: str, message: dict):
        """Send message to clients watching specific camera"""
        if camera_id not in self.camera_connections:
            return
        
        text_message = json.dumps(message)
        disconnected = set()
        
        for connection in self.camera_connections[camera_id]:
            try:
                await connection.send_text(text_message)
            except Exception as e:
                print(f"Error sending message: {e}")
                disconnected.add(connection)
        
        for connection in disconnected:
            self.camera_connections[camera_id].discard(connection)

# Global WebSocket manager
ws_manager = WebSocketManager()