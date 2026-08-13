# CareerPulse Core Engine: High-Performance Resume Intelligence

## 1. Technical Stack

- **Framework:** FastAPI (High-performance API layer)
- **Python:** 3.12 (managed via `uv` for reproducible builds)
- **Authentication & Admin:** PBKDF2-HMAC-SHA256 password hashing (100,000 iterations), 16-byte random salts, HMAC-SHA256 7-day JWT tokens, Admin Router (`/api/v1/admin`)
- **Document & OCR Engine:** `pdfplumber`, `pytesseract` (300 DPI `--psm 3`), `pdf2image`, `OpenCV` (CLAHE & Adaptive Thresholding), hyphen line-wrap normalization
- **Vector Database & Persistence:** Qdrant (HNSW indexing) & PyTorch Tensor Matrix Cache (`dataset_embeddings_cache.pt`)
- **AI/NLP:**
  - `sentence-transformers` (SBERT for 384-dimensional vector embeddings with Section-Aware weighting)
  - Token-Aware Skill Matcher (`is_skill_in_text`) with 150+ tech dictionary
  - `transformers` (Local LLM inference via Qwen 2.5)
  - `bitsandbytes` (4-bit NF4 quantization for GPU efficiency)
- **Real-Time Communication:** Native FastAPI WebSockets & Custom WebRTC P2P Engine
- **Middleware:** CORSMiddleware & Maintenance Mode / Request Telemetry Middleware.

---

## 2. Key Progress

- [x] **Project Architecture:** Modular monolith structure with decoupled service layers.
- [x] **User Authentication:** Sign-In & Sign-Up system (`/signup`, `/login`, `/me`) with PBKDF2 hashing and JWT tokens.
- [x] **Admin Control Console:** Master admin account seeding (`admin@careerpulse.ai`), site settings update, banner publisher & feature flags.
- [x] **UX Telemetry Engine:** Real-time metrics counters, system hardware load (CPU, RAM, Uptime), and activity audit feed (`telemetry_db.json`).
- [x] **Document & OCR Engine:** Multi-column spatial layout reconstruction, table extraction, hyperlink harvesting, hyphen normalization, and 300 DPI dual-pass CLAHE OCR.
- [x] **Top 5 Matching:** Section-Aware SBERT vector similarity search yielding top 5 job recommendations.
- [x] **Degree Filtering:** Automatic degree qualification extraction (`B.Tech`, `B.Sc`, etc.) & degree group matching (`DEGREE_GROUPS`).
- [x] **Local AI Inference:** Full support for 4-bit quantized local Qwen 2.5 execution.
- [x] **WebRTC Expert Subsystem:** Native WebSocket signaling hub and AI Expert Briefing Dossier synthesis.
- [x] **Unified API:** Single `/analyze` endpoint for end-to-end resume intelligence.
- [ ] **Extended Format Support:** Native ingestion of `.docx` and `.txt` files.

---

## Architectural Philosophy

The Core Engine follows a **Modular Monolith** architecture. While deployed as a single FastAPI application, internal logic is strictly decoupled into independent domains:

1. **Authentication Layer (`auth`)**: Handles user registration, login, PBKDF2 password hashing, salt management, JWT token signing, and profile retrieval.
2. **Admin Control Layer (`admin`)**: Admin login, site configuration settings, feature flags, user deletion, and audit log purging.
3. **Telemetry Layer (`telemetry`)**: Records platform usage counters, system hardware stats (CPU, RAM, Uptime), and activity audit logs (`telemetry_db.json`).
4. **Extraction Layer (`resume_security`)**: Handles raw document conversion, spatial multi-column layout reconstruction, table extraction, hyperlink harvesting, hyphen normalization, and 300 DPI dual-pass CLAHE preprocessed OCR.
5. **Persistence Layer (`data_layer`)**: Manages vector search with Qdrant and cached PyTorch tensor matrix (`(5000, 384)`).
6. **Inference Layer (`smart_match` & `llm_service`)**: Orchestrates SBERT vector embeddings, token-aware skill matching (`is_skill_in_text`), degree group filtering, and local Qwen 2.5 LLMs.
7. **Real-Time Stage (`expert_session`)**: Manages WebRTC P2P audio/video signaling and AI Expert Briefing Dossier compilation.
8. **API Layer (`main.py`)**: Exposes the unified `/analyze` gateway and subsystem routers.

---

## Service Deep Dives

### `auth/` (Authentication)
- **`router.py`**: `/api/v1/auth/signup`, `/api/v1/auth/login`, and `/api/v1/auth/me`.
- **`service.py`**: PBKDF2 password hashing (100,000 iterations), HMAC SHA256 token encoding/decoding, user seeding, and persistent database storage (`users_db.json`).

### `admin/` (Admin Controls)
- **`router.py`**: `/api/v1/admin/login`, `/api/v1/admin/telemetry`, `/api/v1/admin/settings`, `/api/v1/admin/users`, `/api/v1/admin/clear-logs`.

### `telemetry/` (Analytics Engine)
- **`service.py`**: Records usage metrics, psutil system stats (CPU, RAM, Uptime), site settings, and activity audit feed (`telemetry_db.json`).

### `embedding_service.py` (The Mathematical Foundation)
Managed singleton for `SentenceTransformer` (`all-MiniLM-L6-v2`) supporting `*args` and `**kwargs` with CUDA auto-detection.

### `llm_service.py` (The Intelligence Layer)
Local Qwen 2.5 (1.5B/7B) inference service utilizing 4-bit NF4 quantization (`bitsandbytes`) and strict JSON prompt enforcement.
