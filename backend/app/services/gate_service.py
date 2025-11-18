from typing import List, Optional
from app.database.mongo import get_database
from app.models.gate import Gate
from app.services.websocket_manager import ws_manager
import asyncio

class GateService:
    """Service for managing gates and barriers"""
    
    async def create_gate(self, gate: Gate) -> Gate:
        """Create new gate"""
        db = await get_database()
        gate_dict = gate.model_dump()
        
        result = await db.gates.insert_one(gate_dict)
        gate_dict["_id"] = str(result.inserted_id)
        
        return Gate(**gate_dict)
    
    async def get_gate(self, gate_id: str) -> Optional[Gate]:
        """Get gate by ID"""
        db = await get_database()
        gate_dict = await db.gates.find_one({"id": gate_id})
        
        if gate_dict:
            return Gate(**gate_dict)
        return None
    
    async def get_all_gates(self) -> List[Gate]:
        """Get all gates"""
        db = await get_database()
        gates = []
        
        async for gate_dict in db.gates.find():
            gates.append(Gate(**gate_dict))
        
        return gates
    
    async def update_gate(self, gate_id: str, gate_data: dict) -> Optional[Gate]:
        """Update gate"""
        db = await get_database()
        
        result = await db.gates.update_one(
            {"id": gate_id},
            {"$set": gate_data}
        )
        
        if result.modified_count > 0:
            return await self.get_gate(gate_id)
        return None
    
    async def delete_gate(self, gate_id: str) -> bool:
        """Delete gate"""
        db = await get_database()
        result = await db.gates.delete_one({"id": gate_id})
        
        return result.deleted_count > 0
    
    async def open_gate(self, gate_id: str, duration: Optional[int] = None) -> bool:
        """Open gate (trigger NodeMCU relay)"""
        gate = await self.get_gate(gate_id)
        
        if not gate or not gate.is_active:
            return False
        
        # In production, send signal to NodeMCU via HTTP/MQTT
        # For now, just log and broadcast event
        
        open_duration = duration or gate.open_duration
        
        print(f"Opening gate {gate.name} (ID: {gate_id}) for {open_duration} seconds")
        
        # Broadcast gate opened event
        await ws_manager.broadcast_event("gate_opened", {
            "gate_id": gate_id,
            "gate_name": gate.name,
            "duration": open_duration
        })
        
        # TODO: Implement actual NodeMCU control
        # Example: await self._send_nodemcu_command(gate.nodemcu_id, gate.relay_pin, open_duration)
        
        return True
    
    async def test_gate(self, gate_id: str) -> bool:
        """Test gate operation"""
        return await self.open_gate(gate_id, duration=2)

# Global gate service
gate_service = GateService()