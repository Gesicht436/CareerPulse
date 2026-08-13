# CareerPulse: System Architecture & Comprehensive Technical Context

This document provides an exhaustive technical overview, directory blueprint, and subsystem map of the **CareerPulse** repository for developer onboarding, system administration, and architectural reference.

---

## 1. Project Overview

**CareerPulse** is a modern, privacy-first, locally accelerated AI career intelligence platform, ATS simulator, and administrator management portal. It empowers job seekers to analyze resumes against job descriptions, uncover technical skill gaps, obtain degree-matched job recommendations, inspect full job requirements, view structured weekly career roadmaps, and conduct 1-on-1 WebRTC live video sessions with industry mentors. Simultaneously, it provides site administrators with real-time hardware telemetry, active audit logs, announcement publishing capabilities, user account controls, and feature flag management.

---

## 2. Core Value Proposition & Key Capabilities

1. **User Authentication & Session Management**:
   - Secure Sign-In and Sign-Up authentication powered by **PBKDF2-HMAC-SHA256** password hashing with unique 16-byte random salt and 100,000 iterations.
   - HMAC-SHA256 signed 7-day JWT tokens containing user ID, email, and role claims (`user` / `admin`).
   - Persistent user account storage in [users_db.json](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/auth/users_db.json).

2. **Admin Control Console & Real-Time Telemetry Engine**:
   - Master admin hub ([admin.html](file:///C:/Users/mayan/Development/Projects/CareerPulse/web_interface/public/admin.html), `/api/v1/admin`) with default administrative credentials (`admin@careerpulse.ai` / `admin123`).
   - Real-time hardware telemetry via `psutil` (CPU %, RAM MB/%, Uptime) and activity counters (Page Views, Resumes Parsed, WebRTC Calls, Job Searches, Custom JD Evaluations).
   - Global site controls: Live top announcement banner publisher, scheduled maintenance toggle, feature flag controls (Resume Upload, JD Analyzer, Expert Calls), user deletion, and log clearing ([telemetry_db.json](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/telemetry/telemetry_db.json)).

3. **High-Fidelity Document & OCR Extraction Engine**:
   - **Multi-Column & Spatial Reconstruction**: Extracts text with spatial coordinate sorting (`top, x0`) using `pdfplumber` to reconstruct multi-column layouts without line garbling across columns.
   - **Line-Wrap Hyphen Repair**: Automatically normalizes hyphenated split words (`Py-\nthon` $\to$ `Python`).
   - **Table & Grid Parsing**: Parses borderless and bordered tables to preserve structured education, experience, and certification grids into readable lines.
   - **Hyperlink & Annotation Harvesting**: Extracts embedded target URIs (`page.hyperlinks` / `page.annots`) for GitHub, LinkedIn, and portfolio links.
   - **Adaptive 300 DPI Preprocessed OCR**: Employs a 300 DPI dual-pass OCR pipeline (`pdf2image` + OpenCV CLAHE contrast enhancement + Bilateral noise filtering + Adaptive Gaussian Thresholding + `pytesseract` `--psm 3`).

4. **Semantic Top 5 Matching & Degree Group Filtering (Zero-Docker SQLite + PyTorch)**:
   - Section-aware semantic vector search ($0.40 \times \text{Headline} + 0.60 \times \text{Body}$) using SBERT (`all-MiniLM-L6-v2`, 384 dimensions) against embedded SQLite metadata store (`jobs.db`) and PyTorch pre-computed tensor matrix cache (`5000 x 384`). Zero Docker containers or external vector databases required.
   - Educational qualification extractor (`B.Tech`, `B.Sc`, `M.Tech`, `MBA`, `BCA`, `MCA`, `Ph.D`) enforcing strict degree group filtering (`DEGREE_GROUPS`).
   - Token-aware technical skill matcher (`is_skill_in_text`) using a 150+ tech dictionary and regex word-boundary evaluation.

5. **Local Quantized LLM Reasoning & Roadmaps**:
   - Powered by a local **Qwen 2.5** model (`Qwen/Qwen2.5-1.5B-Instruct` or 7B) using `bitsandbytes` 4-bit NormalFloat4 (NF4) quantization.
   - Generates structured JSON feedback: match justifications, identified skill overlaps, missing technical skill gaps, actionable recommendations, and weekly career roadmaps.

6. **1-on-1 WebRTC Live Expert Interaction System**:
   - Peer-to-peer audio/video and chat stage powered by native FastAPI WebSockets (`/api/v1/expert/ws/{room_id}`) and browser `RTCPeerConnection`.
   - Synthesizes an **AI Expert Briefing Dossier** summarizing candidate match scores, security status, skill gaps, and discussion topics for mentors.

7. **Utility-First Frontend Interface**:
   - Responsive web interface constructed with HTML5, Vanilla JavaScript (ES6+), and Tailwind CSS v4 (`@tailwindcss/cli`).

---

## 3. Technology Stack & Dependencies

| Category | Technology / Library | Version / Details | Purpose |
| :--- | :--- | :--- | :--- |
| **Language Runtime** | Python | `>= 3.12` | Core backend runtime |
| **Node Runtime** | Node.js | `>= 20.0` | Frontend build environment |
| **Package Manager** | `uv` | System level | Fast Python dependency management |
| **API Framework** | FastAPI | `>= 0.136.0` | Async web framework & WebSocket routing |
| **Authentication & Admin**| PBKDF2, HMAC-SHA256 JWT | Standard Library | Password hashing & admin JWT sessions |
| **Telemetry Analytics** | `psutil` | System level | Live CPU, RAM & Uptime metrics |
| **Database & Vector Store** | SQLite3 & PyTorch Tensor Matrix | Native / `(5000, 384)` | Zero-Docker embedded SQLite DB with PyTorch tensor matrix ranking |
| **Embeddings** | `sentence-transformers` | `>= 5.4.1` | Loads `all-MiniLM-L6-v2` (384D vectors) |
| **Local LLM** | `transformers`, `bitsandbytes` | `>= 5.5.4` / `>= 0.49.2` | Runs quantized Qwen 2.5 1.5B/7B model |
| **Deep Learning** | PyTorch | `2.10.0+cu130` | GPU acceleration framework via CUDA 13.0 |
| **PDF Extraction** | `pdfplumber` | `>= 0.11.9` | Vector PDF text, column, table & link parsing |
| **OCR Pipeline** | `pdf2image`, `opencv-python`, `pytesseract` | `>= 1.17.0`, `>= 4.13.0`, `>= 0.3.13` | 300 DPI dual-pass preprocessed OCR fallback |
| **Real-Time Stage** | WebSockets, WebRTC | Native | Real-time P2P video/audio signaling and chat |
| **Styling** | Tailwind CSS | `v4.0.0` (`@tailwindcss/cli`) | Utility-first frontend styling |

---

## 4. Complete Project Directory Structure & File Map

```text
CareerPulse/
├── .env                        # Local environment settings (Auth secret, Kaggle API key)
├── .env.example                # Template for environment configuration
├── .gitignore                  # Git exclusion rules (.venv, cache files)
├── .python-version             # Python runtime declaration (3.12)
├── ARCHITECTURE.md             # Master system architecture blueprint
├── EXPERT_INTERACTION_SYSTEM.md# 1-on-1 WebRTC system documentation
├── PROJECT_CONTEXT.md          # Primary onboarding & technical context document (this file)
├── README.md                   # Primary project overview & quickstart guide
├── USER_FEATURES.md            # Detailed feature reference guide
├── pyproject.toml              # Project dependencies & PyTorch CUDA 13.0 index configuration
├── uv.lock                     # Locked exact dependency tree
├── core_engine/                # Core AI & FastAPI Gateway Layer
│   ├── README.md               # Core engine module documentation
│   ├── __init__.py             # Python package marker
│   ├── embedding_service.py    # Singleton SBERT model loader (all-MiniLM-L6-v2)
│   ├── llm_service.py          # Quantized Qwen 2.5 inference service (4-bit NF4)
│   ├── main.py                 # FastAPI Application Gateway, middleware & /analyze endpoint
│   ├── admin/                  # Admin Control Subsystem
│   │   ├── router.py           # Admin endpoints (/login, /telemetry, /settings, /users, /clear-logs)
│   │   └── schemas.py          # AdminLogin & SiteSettingsUpdate Pydantic models
│   ├── auth/                   # Authentication & Session Subsystem
│   │   ├── __init__.py         # Package marker
│   │   ├── router.py           # Auth endpoints (/signup, /login, /me)
│   │   ├── schemas.py          # UserCreate, UserLogin, UserResponse, TokenResponse schemas
│   │   ├── service.py          # PBKDF2 hashing, JWT signing, user JSON database manager
│   │   └── users_db.json       # Persistent user database store
│   ├── data_layer/             # Embedded SQLite Database & Vector Subsystem
│   │   ├── README.md           # Data layer module documentation
│   │   ├── __init__.py         # Package marker
│   │   ├── database.py         # SQLite connection manager, table schema & helper queries
│   │   ├── schemas.py          # JobDescriptionModel schema
│   │   └── service.py          # DataLayerService, section-aware search & tensor cache
│   ├── datasets/               # Local Job Dataset & Tensor Embeddings Cache
│   │   ├── jobs.db                     # Embedded SQLite job descriptions database
│   │   ├── dataset_embeddings_cache.pt # Pre-computed 5,000 x 384 PyTorch tensor embeddings matrix
│   │   └── raw/
│   │       └── job_descriptions.csv    # 1.6M Kaggle job descriptions dataset
│   ├── expert_session/         # Live 1-on-1 WebRTC Expert System
│   │   ├── router.py           # WebSockets signaling router (/ws/{room_id}) & REST endpoints
│   │   ├── schemas.py          # ExpertProfile, BookingRequest, SessionBooking, ExpertAIBriefing schemas
│   │   └── service.py          # ExpertSessionService & briefing synthesis logic
│   ├── resume_security/        # Document & OCR Extraction Engine
│   │   ├── README.md           # Security module documentation
│   │   ├── __init__.py         # Package marker
│   │   ├── router.py           # FastAPI router (/api/v1/security/upload)
│   │   └── service.py          # SecurityService (spatial text, tables, links, dual-pass OCR)
│   ├── smart_match/            # Matching & Career Advice Subsystem
│   │   ├── README.md           # Smart match module documentation
│   │   ├── __init__.py         # Package marker
│   │   ├── router.py           # Endpoints (/match, /match-all, /search-jobs)
│   │   ├── schemas.py          # SmartMatchRequest, SmartMatchResponse, JobMatchResult schemas
│   │   └── service.py          # SmartMatchService combining SBERT + Token Matcher + LLM
│   └── telemetry/              # Telemetry Analytics Subsystem
│       ├── service.py          # Metrics logger, hardware telemetry & audit log manager
├── quality_assurance/          # QA & Test Suite
│   ├── README.md               # QA directory documentation
│   ├── cuda_check.py           # PyTorch CUDA & GPU diagnostic script
│   ├── test_api.py             # Basic API health check test
│   ├── test_auth.py            # Authentication pipeline tests (signup, login, /me)
│   ├── test_main.py            # Gateway route test suite
│   └── test_smart_match.py     # Smart match service test suite
├── scripts/                    # Automation & ETL Pipeline Scripts
│   ├── README.md               # Scripts module documentation
│   ├── __init__.py             # Package marker
│   ├── generate_visuals.py     # Matplotlib system diagram & benchmark generator
│   ├── ingest_qdrant.py        # Dataset cleaner, SQLite database populator & PyTorch matrix generator
│   ├── md_to_docs.py           # Pandoc Markdown to DOCX converter script
│   └── setup_data.py           # Kaggle API automated dataset downloader
└── web_interface/              # Modern Web Presentation Layer
    ├── README.md               # Web interface documentation
    ├── package.json            # Node.js dependencies & scripts (Tailwind v4, Live Server)
    ├── package-lock.json       # Locked Node dependency tree
    └── public/                 # Static web assets & application pages
        ├── admin.html          # Admin Control Console & Telemetry Hub
        ├── analyzer.html       # Direct Job Description Match Tool
        ├── dashboard.html      # Analysis Results & Roadmap Dashboard
        ├── details.html        # Job Details View
        ├── expert_call.html    # Live WebRTC Video Stage & AI Briefing Panel
        ├── index.html          # Primary Landing Page
        ├── login.html          # Interactive Sign-In / Sign-Up Hub
        ├── search.html         # Semantic Job Search View
        ├── upload.html         # Resume Upload Hub
        ├── css/
        │   ├── input.css       # Tailwind CSS v4 input directive
        │   └── style.css       # Compiled output stylesheet
        └── js/
            ├── admin.js        # Admin Control Console & telemetry engine
            ├── analyzer.js     # Direct JD analyzer trigger
            ├── api.js          # Centralized API HTTP client with Bearer Token support
            ├── auth.js         # Sign-In/Sign-Up tab switcher & auth handlers
            ├── dashboard.js    # Recommendation cards, modal & roadmap UI logic
            ├── expert_call.js  # WebRTC peer connection & live chat stage engine
            ├── main.js         # Navigation controller & global announcement banner retriever
            └── upload.js       # File drag-and-drop & /analyze submission engine
```

---

## 5. Key Subsystem Specifications

### 5.1 FastAPI Gateway & Global Middleware (`core_engine/main.py`)
- **Routers Mounted**: `auth` (`/api/v1/auth`), `admin` (`/api/v1/admin`), `security` (`/api/v1/security`), `smart_match` (`/api/v1/smart-match`), `expert` (`/api/v1/expert`).
- **Unified Route `POST /api/v1/analyze`**:
  1. Checks site maintenance mode and resume upload feature flag (`enable_resume_upload`).
  2. Extracts raw resume text via [SecurityService](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/resume_security/service.py).
  3. Detects candidate educational qualification (`B.Tech`, `B.Sc`, `M.Tech`, `MBA`, `BCA`, `MCA`, `Ph.D`).
  4. Queries [SmartMatchService](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/smart_match/service.py) for top 5 degree-matched roles.
  5. Logs `RESUME_ANALYSIS` telemetry event.
  6. Returns security report, detected qualification, and top 5 match objects.

### 5.2 Embedded Data Layer & PyTorch Tensor Matrix (`core_engine/data_layer`)
- [database.py](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/data_layer/database.py):
  - Uses standard library `sqlite3` to manage `core_engine/datasets/jobs.db`. Zero external containers required.
  - Endpoints/Functions: `init_db()`, `save_jobs(jobs)`, `fetch_all_jobs()`, `fetch_job_by_id(job_id)`.
- [service.py](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/data_layer/service.py):
  - `_load_real_dataset_jobs`: Reads job records from local SQLite store (`jobs.db`) or populates automatically from [job_descriptions.csv](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/datasets/raw/job_descriptions.csv).
  - `_get_dataset_embeddings`: Pre-computes and caches 384D SBERT embeddings in [dataset_embeddings_cache.pt](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/datasets/dataset_embeddings_cache.pt).
  - `search_jobs`: Applies educational qualification filter (`DEGREE_GROUPS`) and section-aware vector scoring ($0.40 \times \text{Headline} + 0.60 \times \text{Body}$) using PyTorch tensor operations.

---

## 6. Verification & Running Instructions

### 6.1 Backend Core Engine Launch
```bash
# Sync dependencies via uv
uv sync

# Launch FastAPI Core Engine (runs on http://localhost:8000)
uv run uvicorn core_engine.main:app --reload --host 0.0.0.0 --port 8000
```

### 6.2 Frontend Development Server Launch
```bash
cd web_interface
npm run dev
# Starts Tailwind CSS compilation watch mode and Live Server on http://localhost:8080
```

### 6.3 Automated Test Suite Execution
```bash
uv run python -m pytest quality_assurance/
```
