# CareerPulse Core Engine: High-Performance Resume Intelligence

The **Core Engine** is the backend central nervous system of **CareerPulse**. It orchestrates user authentication, administrative telemetry and site controls, high-fidelity PDF and OCR document extraction, 1.61M zero-Docker embedded vector matching, local quantized LLM reasoning, and real-time WebRTC 1-on-1 expert mentoring with a strict **no-silent-fallbacks** error policy.

---

## 1. Technical Stack

- **Framework:** FastAPI (Asynchronous Python 3.12, managed with `uv`)
- **Authentication & Admin:** Standard library `hashlib.pbkdf2_hmac` (SHA-256, 100,000 iterations, 16-byte random salts), HMAC-SHA256 7-day JWT tokens, Admin Router (`/api/v1/admin`)
- **Telemetry Analytics:** `psutil` system metrics (CPU %, RAM MB/%, Uptime) and activity event logger (`telemetry_db.json`)
- **Document & OCR Engine:** `pdfplumber` (Spatial multi-column coordinate sorting `top, x0`), borderless/bordered table parsing, embedded hyperlink harvesting, regex hyphen line-wrap joining, and 300 DPI dual-pass preprocessed OCR fallback (OpenCV CLAHE + Bilateral Filtering + Adaptive Thresholding + `pytesseract` `--psm 3`)
- **Persistence & Vector Search:** Zero-Docker Embedded SQLite (`jobs.db`, 1.78 GB in WAL mode) & In-Memory PyTorch FP16 Tensor Embeddings Matrix (`embeddings/dataset_embeddings_full.pt`, shape `(1615940, 384)`, ~1.24 GB) + Bitmask Tensor (`embeddings/dataset_meta_full.pt`)
- **Embeddings & AI:**
  - `sentence-transformers` (`all-MiniLM-L6-v2` for 384-dimensional vectors with Section-Aware weighting: $0.40 \times \text{Headline} + 0.60 \times \text{Body}$)
  - Batch SBERT query encoding (`batch_size=2`) for simultaneous headline and body vector calculation
  - Token-Aware Skill Matcher (`is_skill_in_text`) with 150+ tech dictionary and regex word boundaries
  - `transformers` & `bitsandbytes` (Local Qwen 2.5 1.5B/7B inference with 4-bit NF4 quantization)
- **Real-Time Communication:** Native FastAPI WebSockets (`/api/v1/expert/ws/{room_id}`) & Browser `RTCPeerConnection` with automated AI Expert Briefing Dossier synthesis
- **Error Handling Standard:** Strict exception propagation across all layers (no silent fallbacks or fake mock data)

---

## 2. Subsystem Directory Map

```text
core_engine/
├── README.md                   # Core engine documentation (this file)
├── __init__.py                 # Python package marker
├── embedding_service.py        # Shared SBERT singleton loader (all-MiniLM-L6-v2)
├── llm_service.py              # Local Qwen 2.5 4-bit inference layer (strict error policy)
├── main.py                     # FastAPI Gateway, middleware & unified /analyze endpoint
├── admin/                      # Admin Control & Site Management Subsystem
│   ├── README.md               # Admin subsystem documentation
│   ├── router.py               # Admin endpoints (/login, /telemetry, /settings, /users, /clear-logs)
│   └── schemas.py              # AdminLogin & SiteSettingsUpdate schemas
├── auth/                       # Authentication & Session Management Subsystem
│   ├── README.md               # Auth subsystem documentation
│   ├── __init__.py             # Package marker
│   ├── router.py               # Auth endpoints (/signup, /login, /me)
│   ├── schemas.py              # User schemas (UserCreate, UserLogin, UserResponse, TokenResponse)
│   ├── service.py              # PBKDF2 hashing, JWT signing, users_db.json CRUD
│   └── users_db.json           # Persistent user store
├── data_layer/                 # Embedded SQLite Database & 1.61M Vector Subsystem
│   ├── README.md               # Data layer documentation
│   ├── __init__.py             # Package marker
│   ├── database.py             # SQLite connection manager & 18-column schema in WAL mode
│   ├── schemas.py              # JobDescriptionModel & CompanyProfileModel schemas
│   └── service.py              # DataLayerService, 1.61M vector ranking & degree bitmasking
├── datasets/                   # Datasets & 1.61M Precomputed Embeddings
│   ├── README.md               # Datasets documentation
│   ├── jobs.db                 # Embedded SQLite jobs database (1.78 GB, 1.61M rows)
│   ├── embeddings/             # Automatically generated vector embeddings folder
│   │   ├── dataset_embeddings_full.pt # (1615940, 384) PyTorch FP16 tensor matrix (1.24 GB)
│   │   ├── dataset_meta_full.pt # Job IDs and Degree Bitmask Tensor (43 MB)
│   │   └── cache_checkpoints/  # Intermediate chunk checkpointing folder
│   ├── processed/              # Automatically generated processed data folder
│   │   └── cleaned_job_descriptions.csv # Cleaned & normalized 1.61M dataset (1.39 GB)
│   └── raw/
│       └── job_descriptions.csv # Raw 1.6M Kaggle job descriptions dataset
├── expert_session/             # Live 1-on-1 WebRTC Expert Mentorship System
│   ├── README.md               # Expert session documentation
│   ├── router.py               # WebSockets signaling router & REST endpoints
│   ├── schemas.py              # ExpertProfile, BookingRequest, SessionBooking, ExpertAIBriefing
│   └── service.py              # ExpertSessionService & briefing synthesis
├── resume_security/            # Document & OCR Extraction Engine
│   ├── README.md               # Extraction & OCR documentation
│   ├── __init__.py             # Package marker
│   ├── router.py               # FastAPI router (/api/v1/security/upload)
│   └── service.py              # SecurityService (spatial text, tables, links, dual-pass OCR)
├── smart_match/                # Matching & Career Advice Subsystem
│   ├── README.md               # Smart match documentation
│   ├── __init__.py             # Package marker
│   ├── router.py               # Endpoints (/match, /match-all, /search-jobs)
│   ├── schemas.py              # SmartMatchRequest, SmartMatchResponse, JobMatchResult, MultiJobMatchResponse
│   └── service.py              # SBERT Scoring + Token Matcher + LLM Reasoning
└── telemetry/                  # Telemetry Analytics Subsystem
    ├── README.md               # Telemetry subsystem documentation
    ├── service.py              # psutil hardware metrics & audit event logger
    └── telemetry_db.json       # Persistent counters, settings & audit logs store
```

---

## 3. Subsystem Breakdown & Error Handling Guarantees

### 1. Unified Gateway (`main.py`)
- Mounts all sub-routers under `/api/v1/*`.
- Exposes `POST /api/v1/analyze` to execute the full end-to-end pipeline:
  1. Maintenance mode & feature flag check (`enable_resume_upload`).
  2. Multi-column PDF parsing & OCR extraction (`SecurityService`).
  3. **Strict Validation**: Rejects empty or unreadable PDFs ($< 20$ characters) with HTTP `400 Bad Request`.
  4. Automatic candidate educational qualification detection (`B.Tech`, `B.Sc`, `MBA`, `MCA`, etc.) or assigns `"Unspecified"`.
  5. Top 5 job recommendations retrieval across the 1.61M dataset via section-aware vector scoring and degree bitmask filtering (`SmartMatchService`).
  6. Telemetry event logging (`RESUME_ANALYSIS`).
  7. Returns structured payload with detected degree, security report, top 5 recommendations, and deep ATS analysis.
  8. Propagates explicit HTTP status codes: `400` (bad input/validation), `403` (feature disabled), `503` (missing dataset/maintenance), `500` (internal execution failure).

### 2. Authentication & Admin (`auth/` & `admin/`)
- User onboarding and login via PBKDF2-HMAC-SHA256 (100,000 rounds).
- Stateless 7-day JWT tokens containing user ID, email, and role (`user` vs `admin`).
- Administrative control console (`/api/v1/admin`) with default credentials (`admin@careerpulse.ai` / `admin123`).
- Strict JSON database error handling: Corrupted user database files raise explicit `RuntimeError` rather than silently wiping data.

### 3. Data & Vector Store (`data_layer/` & `datasets/`)
- **Single-Tier 1.61M Architecture**: Zero Docker containers, leveraging native `sqlite3` (`jobs.db`, 1.78 GB) and in-memory PyTorch FP16 matrix (`dataset_embeddings_full.pt`, 1.24 GB).
- Sub-250ms similarity queries across all 1,615,940 jobs using parallel PyTorch tensor dot products (`torch.matmul`) with section-aware weighting ($0.40 \times \text{Headline} + 0.60 \times \text{Body}$).
- High-speed indexed batch retrieval from SQLite (`fetch_jobs_by_ids`).
- **Strict Data Policies**:
  - Missing vector matrix or SQLite database raises explicit `FileNotFoundError`.
  - Zero matching jobs under strict qualification filter raises explicit `ValueError`.

### 4. Matching & Local LLM (`smart_match/` & `llm_service.py`)
- Token-aware skill matcher (`is_skill_in_text`) using 150+ tech term dictionary.
- Calibrated 50/50 blended ATS scoring (Vector Alignment + Skill Overlap).
- Local Qwen 2.5 (1.5B/7B) quantized to 4-bit NF4 generating structured JSON advice and weekly learning roadmaps.
- **Strict Inference Policy**: If LLM generation or JSON parsing fails, raises explicit `RuntimeError` with root cause (zero fake mock data).

### 5. Document Extraction (`resume_security/`)
- Spatial layout sorting (`pdfplumber` words by `top, x0`) preventing cross-column text merging.
- Structured table parsing, embedded URI harvesting, and hyphen line-wrap repair.
- 300 DPI dual-pass preprocessed OCR fallback (OpenCV CLAHE + Bilateral Filter + Adaptive Thresholding + `pytesseract`).
- **Strict Extraction Policy**: Unreadable documents raise `ValueError`; OCR execution failures raise `RuntimeError` referencing system dependencies (Tesseract / Poppler).

### 6. Live Mentorship Stage (`expert_session/`)
- WebSocket signaling router (`/api/v1/expert/ws/{room_id}`) supporting SDP offer/answer exchange, ICE candidates, and real-time room chat.
- Automated synthesis of **AI Expert Briefing Dossier** for mentors.
- **Strict Briefing Policy**: Briefing synthesis endpoint `/briefing/{room_id}` strictly requires valid candidate analysis data, returning HTTP `400` if missing.

### 7. Telemetry & Analytics (`telemetry/`)
- Real-time `psutil` CPU/RAM/Uptime metrics.
- Platform activity counters (Page Views, Resumes Analyzed, Calls, Searches, JD Evaluations).
- Persistent JSON configuration and audit log feed (`telemetry_db.json`).

---

## 4. Running the Core Engine

```bash
# Sync dependencies
uv sync

# Launch development server
uv run uvicorn core_engine.main:app --reload --host 0.0.0.0 --port 8000
```
