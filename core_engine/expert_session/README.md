# 1-on-1 WebRTC Live Expert Interaction Subsystem

The `core_engine/expert_session` module orchestrates real-time 1-on-1 audio/video sessions and candidate mentorship tools for **CareerPulse**. It combines peer-to-peer WebRTC signaling via FastAPI WebSockets with an automated **AI Expert Briefing Dossier** synthesis engine.

---

## 1. Technical Stack & Architecture

- **Signaling Server:** FastAPI WebSockets (`/api/v1/expert/ws/{room_id}`)
- **Peer-to-Peer Protocol:** Browser `RTCPeerConnection` with STUN server discovery
- **Real-Time Stage:** Bidirectional WebSockets for SDP offer/answer exchange, ICE candidate routing, and in-room chat messages
- **Intelligence Integration:** Automatically extracts candidate resume audit findings, ATS score, and Qwen LLM learning roadmaps into an **AI Expert Briefing Dossier** for industry mentors
- **Strict Validation:** Requires genuine candidate analysis payload to synthesize briefing dossier (returns HTTP `400 Bad Request` if missing)

---

## 2. API & WebSocket Endpoints

| Method / Protocol | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/expert/list` | Retrieves available industry expert profiles and domains |
| `POST` | `/api/v1/expert/book` | Books a 1-on-1 mentoring session and generates unique `room_id` |
| `GET` | `/api/v1/expert/booking/{identifier}` | Retrieves booking status and details by booking ID or room ID |
| `POST` | `/api/v1/expert/briefing/{room_id}` | Generates a synthesized AI Briefing Dossier from resume analysis data |
| `WebSocket` | `/api/v1/expert/ws/{room_id}` | Real-time signaling hub for WebRTC peer connection and live room chat |

---

## 3. Directory Structure

```text
core_engine/expert_session/
├── README.md       # Subsystem documentation (this file)
├── router.py       # FastAPI REST endpoints & WebSocket room manager
├── schemas.py      # Pydantic models (ExpertProfile, BookingRequest, SessionBooking, ExpertAIBriefing)
└── service.py      # ExpertSessionService, mock experts store, and AI Briefing synthesis
```

---

## 4. Key Components

### `router.py`
- **`ConnectionManager`**: Manages active WebSocket connections per `room_id`, broadcasting SDP offers, answers, ICE candidates, and chat payloads between connected peers.
- **`websocket_endpoint(websocket, room_id)`**: Handles WebSocket lifecycle, client registration, message relaying, and disconnect cleanup.
- **`get_ai_briefing(room_id, payload)`**: Validates analysis payload and returns `ExpertAIBriefing` (raises HTTP 400 on invalid payload).

### `service.py` (`ExpertSessionService`)
- **`get_all_experts()`**: Returns registered industry expert profiles (AI Architecture, Cybersecurity, Scalable Systems).
- **`create_booking(req)`**: Validates expert availability and issues persistent `booking_id` and WebRTC `room_id`.
- **`generate_ai_briefing(candidate_name, analysis_data)`**: Automatically compiles candidate's:
  - Latest Target Role & Match Score
  - Document Security Status
  - Matched vs. Missing Technical Skills
  - Tailored Weekly Learning Roadmap
  - Suggested Technical Discussion Points for the mentor

### `schemas.py`
- **`ExpertProfile`**: Profile schema (`id`, `name`, `title`, `company`, `domain`, `bio`, `rating`, `total_sessions`, `avatar_url`).
- **`BookingRequest`**: Request schema (`expert_id`, `applicant_name`, `applicant_email`, `scheduled_time`).
- **`SessionBooking`**: Booking record (`id`, `room_id`, `expert`, `applicant_name`, `status`, `created_at`).
- **`ExpertAIBriefing`**: Structured dossier schema passed to the expert stage sidebar (`overall_match_score`, `matched_skills`, `missing_skills`, `recommended_roadmap`, `key_discussion_points`).
