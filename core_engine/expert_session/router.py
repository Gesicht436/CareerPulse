from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Body
from typing import Dict, List, Any
import json
from core_engine.expert_session.schemas import BookingRequest, SessionBooking, ExpertProfile, ExpertAIBriefing
from core_engine.expert_session.service import expert_session_service

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        # Maps room_id -> list of active WebSocket connections
        self.rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = []
        self.rooms[room_id].append(websocket)
        print(f"DEBUG: WebSocket connected to room '{room_id}'. Total peers: {len(self.rooms[room_id])}")

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.rooms:
            if websocket in self.rooms[room_id]:
                self.rooms[room_id].remove(websocket)
            if not self.rooms[room_id]:
                del self.rooms[room_id]
        print(f"DEBUG: WebSocket disconnected from room '{room_id}'")

    async def broadcast_to_others(self, sender_socket: WebSocket, room_id: str, message: dict):
        if room_id in self.rooms:
            for connection in self.rooms[room_id]:
                if connection != sender_socket:
                    await connection.send_json(message)

manager = ConnectionManager()

# --- REST ENDPOINTS ---

@router.get("/list", response_model=List[ExpertProfile])
async def list_experts():
    """
    Returns the list of verified industry experts available for 1-on-1 sessions.
    """
    return expert_session_service.get_all_experts()

@router.post("/book", response_model=SessionBooking)
async def create_booking(request: BookingRequest):
    """
    Creates a new 1-on-1 booking session and returns the WebRTC room credentials.
    """
    try:
        return expert_session_service.create_booking(request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/booking/{identifier}", response_model=SessionBooking)
async def get_booking_details(identifier: str):
    """
    Retrieves booking details by booking ID or room ID.
    """
    booking = expert_session_service.get_booking(identifier)
    if not booking:
        raise HTTPException(status_code=404, detail="Session booking not found.")
    return booking

@router.post("/briefing/{room_id}", response_model=ExpertAIBriefing)
async def get_ai_briefing(room_id: str, payload: Dict[str, Any] = Body(default={})):
    """
    Generates an AI Expert Briefing Dossier for the expert prior to or during the call.
    """
    booking = expert_session_service.get_booking(room_id)
    candidate_name = booking.applicant_name if booking else "Applicant"
    briefing = expert_session_service.generate_ai_briefing(candidate_name, payload)
    return briefing

# --- WEBRTC WEBSOCKET SIGNALING ENDPOINT ---

@router.websocket("/ws/{room_id}")
async def webrtc_signaling_endpoint(websocket: WebSocket, room_id: str):
    """
    FastAPI WebSocket endpoint handling WebRTC P2P signaling (Offer, Answer, ICE Candidates, Chat).
    """
    await manager.connect(websocket, room_id)
    
    # Notify peer if another participant is already in the room
    peer_count = len(manager.rooms.get(room_id, []))
    await websocket.send_json({
        "type": "room_joined",
        "room_id": room_id,
        "peer_count": peer_count
    })

    if peer_count > 1:
        # Broadcast readiness to negotiate
        await manager.broadcast_to_others(websocket, room_id, {
            "type": "peer_ready",
            "message": "A peer has joined the session."
        })
        try:
            from core_engine.telemetry.service import telemetry_service
            telemetry_service.log_event("EXPERT_CALL_START", f"WebRTC 1-on-1 Mentorship session connected in room '{room_id}'.", {"room_id": room_id, "peers": peer_count})
        except Exception:
            pass

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")
            
            # Relay WebRTC signaling messages directly to the other peer in the room
            if msg_type in ["offer", "answer", "ice_candidate", "chat_message", "hangup"]:
                await manager.broadcast_to_others(websocket, room_id, data)
            else:
                print(f"DEBUG: Unknown message type '{msg_type}' received in room {room_id}")

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        await manager.broadcast_to_others(websocket, room_id, {
            "type": "peer_disconnected",
            "message": "Peer has left the session."
        })
    except Exception as e:
        print(f"DEBUG ERROR: WebSocket error in room {room_id}: {e}")
        manager.disconnect(websocket, room_id)
