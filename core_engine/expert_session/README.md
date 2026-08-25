# 1-on-1 WebRTC Live Expert Interaction Subsystem

The `core_engine/expert_session` module orchestrates real-time 1-on-1 audio/video sessions and candidate mentorship tools for **CareerPulse**. It combines peer-to-peer WebRTC signaling via FastAPI WebSockets with an automated **AI Expert Briefing Dossier** synthesis engine and live telemetry tracking.

---

## 1. Technical Stack & Architecture

- **Signaling Server:** FastAPI WebSockets (`/api/v1/expert/ws/{room_id}`) with multi-peer room connection management
- **Peer-to-Peer Protocol:** Browser `RTCPeerConnection` with Google STUN server discovery (`stun:stun.l.google.com:19302`)
- **Real-Time Signaling Payloads:** Bidirectional WebSockets relaying SDP offers, answers, ICE candidates, live chat messages, and hangup notifications
- **Intelligence Integration:** Automatically synthesizes candidate resume audit findings, calibrated ATS score, missing skill gaps, and Qwen LLM learning roadmaps into an **AI Expert Briefing Dossier**
- **Strict Validation:** Requires genuine candidate analysis payload to synthesize briefing dossier (returns HTTP `400 Bad Request` on empty/corrupt analysis)
- **Telemetry Event Logging:** Automatically records `EXPERT_CALL_START` events in `telemetry_db.json` when peers connect

---

## 2. API & WebSocket Endpoints

| Method / Protocol | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/expert/list` | Retrieves available industry expert profiles and domains | `200` |
| `POST` | `/api/v1/expert/book` | Books a 1-on-1 mentoring session and generates unique `room_id` | `200`, `404` |
| `GET` | `/api/v1/expert/booking/{identifier}` | Retrieves booking status and details by booking ID or room ID | `200`, `404` |
| `POST` | `/api/v1/expert/briefing/{room_id}` | Generates a synthesized AI Briefing Dossier from resume analysis data | `200`, `400` |
| `WebSocket` | `/api/v1/expert/ws/{room_id}` | Real-time signaling hub for WebRTC peer connection and live room chat | `101 Switching Protocols` |

---

## 3. Directory Structure

```text
core_engine/expert_session/
├── README.md       # Subsystem documentation (this file)
├── __init__.py     # Package marker
├── router.py       # FastAPI REST endpoints & WebSocket room manager (ConnectionManager)
├── schemas.py      # Pydantic models (ExpertProfile, BookingRequest, SessionBooking, ExpertAIBriefing)
└── service.py      # ExpertSessionService, verified experts store, and AI Briefing synthesis
```

---

## 4. Key Components & Data Flow

### `router.py`
- **`ConnectionManager`**:
  - `connect(websocket, room_id)`: Registers active WebSocket connections per room.
  - `disconnect(websocket, room_id)`: Cleans up disconnected sockets and empties empty rooms.
  - `broadcast_to_others(sender, room_id, message)`: Relays WebRTC signaling payloads to the remote peer.
- **`webrtc_signaling_endpoint(websocket, room_id)`**:
  - Sends `room_joined` event with active `peer_count`.
  - Broadcasts `peer_ready` when a second participant joins.
  - Relays `offer`, `answer`, `ice_candidate`, `chat_message`, and `hangup` message types.
  - Logs `EXPERT_CALL_START` event to `telemetry_service`.
- **`get_ai_briefing(room_id, payload)`**: Validates analysis payload and returns `ExpertAIBriefing` (raises HTTP `400` if missing analysis).

### `service.py` (`ExpertSessionService`)
- **`get_all_experts()`**: Returns registered industry mentors:
  - **Alex Rivera**: Principal AI Architect (DeepMind / Google) — AI/ML & LLM systems.
  - **Dr. Elena Rostova**: Staff Security Engineer (CrowdStrike) — Cybersecurity & Defensive Audit.
  - **Marcus Vance**: VP of Engineering (Stripe) — Scalable Backend & System Design.
- **`create_booking(req)`**: Validates expert availability and issues unique `booking_id` (`book-<uuid>`) and WebRTC `room_id` (`room-<uuid>`).
- **`generate_ai_briefing(candidate_name, analysis_data)`**: Compiles:
  - Latest Target Role & Match Score
  - Document Security Status (`Verified Clean` / `Flagged`)
  - Matched Technical Strengths & Missing Skill Gaps
  - Tailored 4-Week Learning Roadmap
  - Suggested Key Discussion Points for the mentor

### `schemas.py`
- **`ExpertProfile`**: Profile schema (`id`, `name`, `title`, `company`, `domain`, `bio`, `rating`, `total_sessions`, `avatar_url`).
- **`BookingRequest`**: Request schema (`expert_id`, `applicant_name`, `applicant_email`, `scheduled_time`, `notes`).
- **`SessionBooking`**: Booking record (`id`, `room_id`, `expert`, `applicant_name`, `applicant_email`, `scheduled_time`, `status`, `created_at`).
- **`ExpertAIBriefing`**: Structured dossier passed to the expert stage sidebar (`candidate_name`, `latest_job_title`, `overall_match_score`, `security_status`, `matched_skills`, `missing_skills`, `recommended_roadmap`, `key_discussion_points`).
