from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import ws_manager
import asyncio

router = APIRouter(prefix="/api/system", tags=["system"])

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "EvoPlate system is running"}

@router.get("/ping")
async def ping():
    """Ping endpoint"""
    return {"pong": True}

@router.websocket("/ws/events")
async def events_websocket(websocket: WebSocket):
    """WebSocket endpoint for system events"""
    await ws_manager.connect_events(websocket)
    
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            # Echo back for ping/pong
            await websocket.send_text(data)
    
    except WebSocketDisconnect:
        ws_manager.disconnect_events(websocket)
    except Exception as e:
        print(f"Events WebSocket error: {e}")
        ws_manager.disconnect_events(websocket)