# CareerPulse: AI-Powered Career Optimization & Semantic Job Matching

**CareerPulse** is a modern, UX-first career intelligence platform that leverages local Large Language Models (LLMs), embedded vector search, high-fidelity document parsing, and real-time interaction systems to provide job seekers with deep, actionable insights into their professional alignment. Unlike traditional ATS systems that rely on rigid keyword matching, CareerPulse understands the **semantic context** of your experience, reconstructing complex resume layouts, identifying skill gaps, and generating personalized learning roadmaps alongside live 1-on-1 expert guidance, secure user accounts, and administrative site management controls.

---

## Core Value Proposition

CareerPulse delivers seven foundational pillars:

1. **User Authentication & Session Persistence**: Secure Sign-In and Sign-Up authentication powered by standard library `hashlib.pbkdf2_hmac` with SHA-256 (100,000 iterations, 16-byte random salts) and 7-day HMAC-SHA256 JWT tokens.
2. **UX-First Telemetry & Admin Control Console**: Captures real-time candidate alignment telemetry, platform usage counters (Users, Resumes Parsed, WebRTC Calls, Job Searches, JD Evaluations), system hardware load (CPU %, RAM MB/%, Uptime via `psutil`), activity audit logs, live top announcement banner publishing, and instant feature flag toggles (`admin@careerpulse.ai`).
3. **Semantic-First Alignment & Top 5 Recommendations**: Powered by **SBERT (Sentence-BERT)** (`all-MiniLM-L6-v2`, 384 dimensions) and Section-Aware Weighted Vector Search ($0.40 \times \text{Headline} + 0.60 \times \text{Body}$), the engine computes top 5 matched job recommendations across a 1.6M row job database with full job description inspection modals (`#job-inspect-modal`).
4. **Educational Qualification Degree Filtering**: Extracts degree qualifications (`B.Tech`, `M.Tech`, `B.Sc`, `M.Sc`, `BCA`, `MCA`, `B.Com`, `MBA`, `Ph.D`) directly from resume text and enforces degree group filtering (`DEGREE_GROUPS`) with an interactive dashboard filter toggle button (**"Disable Qualification Filter"** / **"Enable Qualification Filter"**).
5. **High-Fidelity Document & OCR Intelligence**: Features a specialized PDF parsing engine that reconstructs multi-column spatial layouts (`pdfplumber` sorted by `top, x0`), extracts structured tables, harvests embedded hyperlinks/annotations (GitHub, LinkedIn, portfolios), normalizes line-wrap hyphens, and executes a 300 DPI dual-pass preprocessed OCR fallback (OpenCV CLAHE + Bilateral Filtering + Adaptive Thresholding + `pytesseract` `--psm 3`).
6. **Local Quantized LLM Reasoning & Roadmaps**: Powered by local **Qwen 2.5** (1.5B/7B) with 4-bit NormalFloat4 (NF4) quantization via `bitsandbytes`, producing structured JSON justifications, skill gaps, actionable recommendations, and multi-week learning roadmaps.
7. **1-on-1 WebRTC Live Mentorship Stage**: Native FastAPI WebSocket signaling hub (`/api/v1/expert/ws/{room_id}`) paired with browser `RTCPeerConnection` for real-time video/audio and live chat, featuring an automated **AI Expert Briefing Dossier** compiled for mentors.

---

## Unified Technical Stack

The project is architected as a high-performance **Modular Monolith**, split between a specialized AI backend and a modern, utility-first frontend.

### **Backend (Core Engine)**

- **API Framework**: FastAPI (Asynchronous Python 3.12)
- **Authentication & Admin Control**: PBKDF2-HMAC-SHA256 password hashing, HMAC-SHA256 JWT tokens, Admin Router (`/api/v1/admin`)
- **Persistence & Vector Store**: Zero-Docker Embedded SQLite (`jobs.db`) & PyTorch Pre-Computed Tensor Embeddings Matrix (`dataset_embeddings_cache.pt`, shape `(5000, 384)`)
- **Embedding Model**: `all-MiniLM-L6-v2` via `sentence-transformers` (384-dimensional semantic vectors)
- **Local LLM**: Qwen 2.5 1.5B/7B (Quantized via `bitsandbytes` NF4 4-bit)
- **Deep Learning Framework**: PyTorch with CUDA 13.0 GPU acceleration
- **Document & OCR Engine**: `pdfplumber`, `pdf2image`, `pytesseract` (300 DPI, `--psm 3`), `OpenCV` (CLAHE, Bilateral Filtering & Adaptive Thresholding)
- **Real-Time Communications**: Native FastAPI WebSockets & Custom WebRTC P2P Engine
- **Telemetry Analytics**: `psutil` system metrics and JSON audit feed (`telemetry_db.json`)

### **Frontend (Web Interface)**

- **Styling**: Tailwind CSS v4 (Utility-first, `@tailwindcss/cli` build pipeline)
- **Logic**: Vanilla ES6+ JavaScript (Zero-dependency, high-speed execution)
- **Architecture**: Static-site generation with dynamic API orchestration, top 5 recommendation cards, full job description inspection modal, interactive qualification toggle button, and Admin Control Portal (`admin.html`).

### **Automation & Ops**

- **Dependency Management**: `uv` (Fast Python package manager)
- **Visualization**: `matplotlib`, `numpy` (Programmatic technical diagrams)
- **Documentation**: `pandoc` / `pypandoc` (Cross-format conversion)

---

## Current Project Status

| Milestone | Feature | Status |
| :--- | :--- | :--- |
| **Authentication** | Sign-In & Sign-Up system (PBKDF2, JWT tokens, `users_db.json`) | [x] Completed |
| **Admin Control** | Admin portal (`admin.html`), telemetry metrics, audit logs, feature flags | [x] Completed |
| **Document Processing** | Multi-column layout reconstruction, Table & Hyperlink harvesting | [x] Completed |
| **OCR Intelligence** | 300 DPI Dual-Pass Preprocessed OCR (CLAHE + Adaptive Thresholding) | [x] Completed |
| **Data Layer** | Zero-Docker Embedded SQLite (`jobs.db`) & Cached PyTorch Tensor Matrix (`(5000, 384)`) | [x] Completed |
| **Matching Engine** | Top 5 Job Recommendations, SBERT Section-Aware Scoring & Token-Aware Skill Matcher | [x] Completed |
| **Degree Filtering** | Automatic Degree Extraction (`B.Tech`, `B.Sc`, etc.) & Interactive Dashboard Filter Toggle | [x] Completed |
| **Job Inspection** | Full Job Description Inspection Modal (`#job-inspect-modal`) & Action Links | [x] Completed |
| **Intelligence** | Local LLM Integration (Qwen 2.5) with 4-bit quantization | [x] Completed |
| **Expert System** | WebRTC 1-on-1 Peer-to-Peer Live Video & AI Briefing Dossier | [x] Completed |
| **Web UI** | Responsive Dashboard, Upload Hub, Job Search, Admin Hub & Live Stage | [x] Completed |
| **Orchestration** | Unified End-to-End Analysis Pipeline (`/api/v1/analyze`) | [x] Completed |

---

## Complete Project Directory Structure

```text
CareerPulse/
├── ARCHITECTURE.md                 # Master system architecture blueprint
├── EXPERT_INTERACTION_SYSTEM.md    # 1-on-1 WebRTC system documentation
├── PROJECT_CONTEXT.md              # Primary technical context & onboarding reference
├── README.md                       # Primary project overview & quickstart guide (this file)
├── USER_FEATURES.md                # Comprehensive user feature catalog
├── pyproject.toml                  # Project dependencies & PyTorch CUDA 13.0 index configuration
├── uv.lock                         # Locked exact dependency tree
│
├── core_engine/                    # Backend Central Nervous System
│   ├── README.md                   # Core engine module documentation
│   ├── __init__.py                 # Python package marker
│   ├── embedding_service.py        # Shared SBERT singleton loader (all-MiniLM-L6-v2)
│   ├── llm_service.py              # Local Qwen 2.5 4-bit inference layer
│   ├── main.py                     # FastAPI Gateway, middleware & /analyze endpoint
│   ├── admin/                      # Admin Control Subsystem
│   │   ├── README.md               # Admin subsystem documentation
│   │   ├── router.py               # Admin endpoints (/login, /telemetry, /settings, /users, /clear-logs)
│   │   └── schemas.py              # AdminLogin & SiteSettingsUpdate schemas
│   ├── auth/                       # Authentication & Session Subsystem
│   │   ├── README.md               # Auth subsystem documentation
│   │   ├── __init__.py             # Package marker
│   │   ├── router.py               # Auth endpoints (/signup, /login, /me)
│   │   ├── schemas.py              # User schemas (UserCreate, UserLogin, TokenResponse)
│   │   ├── service.py              # PBKDF2 hashing, JWT signing, users_db.json CRUD
│   │   └── users_db.json           # Persistent user store
│   ├── data_layer/                 # Embedded SQLite Database & Vector Subsystem
│   │   ├── README.md               # Data layer documentation
│   │   ├── __init__.py             # Package marker
│   │   ├── database.py             # SQLite connection manager & queries
│   │   ├── schemas.py              # JobDescriptionModel schema
│   │   └── service.py              # DataLayerService, section-aware search & tensor cache
│   ├── datasets/                   # Datasets & Cached Embeddings
│   │   ├── README.md               # Datasets documentation
│   │   ├── jobs.db                 # Embedded SQLite job descriptions database
│   │   ├── dataset_embeddings_cache.pt # 5,000 x 384 PyTorch tensor embeddings matrix
│   │   └── raw/
│   │       └── job_descriptions.csv # 1.6M Kaggle job descriptions dataset
│   ├── expert_session/             # Live 1-on-1 WebRTC Expert System
│   │   ├── README.md               # Expert session documentation
│   │   ├── router.py               # WebSockets signaling router & REST endpoints
│   │   ├── schemas.py              # ExpertProfile, BookingRequest, ExpertAIBriefing schemas
│   │   └── service.py              # ExpertSessionService & briefing synthesis
│   ├── resume_security/            # Document & OCR Extraction Engine
│   │   ├── README.md               # Extraction & OCR documentation
│   │   ├── __init__.py             # Package marker
│   │   ├── router.py               # FastAPI router (/api/v1/security/upload)
│   │   └── service.py              # SecurityService (spatial text, tables, links, dual-pass OCR)
│   ├── smart_match/                # Matching & Career Advice Subsystem
│   │   ├── README.md               # Smart match documentation
│   │   ├── __init__.py             # Package marker
│   │   ├── router.py               # Endpoints (/match, /match-all, /search-jobs)
│   │   ├── schemas.py              # SmartMatchRequest, SmartMatchResponse, JobMatchResult
│   │   └── service.py              # SBERT Scoring + Token Matcher + LLM Reasoning
│   └── telemetry/                  # Telemetry Analytics Subsystem
│       ├── README.md               # Telemetry subsystem documentation
│       ├── service.py              # psutil hardware metrics & audit event logger
│       └── telemetry_db.json       # Persistent counters, settings & audit logs store
│
├── quality_assurance/              # QA Test Suite & Hardware Diagnostics
│   ├── README.md                   # QA documentation
│   ├── cuda_check.py               # PyTorch CUDA & GPU diagnostic script
│   ├── test_api.py                 # Basic API health check test
│   ├── test_auth.py                # Authentication pipeline tests (signup, login, /me)
│   ├── test_main.py                # Gateway route test suite
│   └── test_smart_match.py         # Smart match service test suite
│
├── scripts/                        # Automation & Data Pipelines
│   ├── README.md                   # Scripts documentation
│   ├── __init__.py                 # Package marker
│   ├── generate_visuals.py         # Matplotlib system diagram & benchmark generator
│   ├── ingest_qdrant.py            # Dataset populator & PyTorch tensor matrix generator
│   ├── md_to_docs.py               # Pandoc Markdown to DOCX converter script
│   └── setup_data.py               # Kaggle dataset automated downloader
│
└── web_interface/                  # Modern Web Presentation Layer
    ├── README.md                   # Web interface documentation
    ├── package.json                # Node.js dependencies & scripts (Tailwind v4, Live Server)
    ├── package-lock.json           # Locked Node dependency tree
    └── public/                     # Static web assets & application pages
        ├── admin.html              # Admin Control Console & Telemetry Hub
        ├── analyzer.html           # Direct Job Description Match Tool
        ├── dashboard.html          # Analysis Results & Roadmap Dashboard
        ├── details.html            # Job Details View
        ├── expert_call.html        # Live WebRTC Video Stage & AI Briefing Panel
        ├── index.html              # Primary Landing Page
        ├── login.html              # Interactive Sign-In / Sign-Up Hub
        ├── search.html             # Semantic Job Search View
        ├── upload.html             # Resume Upload Hub
        ├── css/
        │   ├── input.css           # Tailwind CSS v4 input directive
        │   └── style.css           # Compiled output stylesheet
        └── js/
            ├── admin.js            # Admin Control Console & telemetry engine
            ├── analyzer.js         # Direct JD analyzer trigger
            ├── api.js              # Centralized API HTTP client with Bearer Token support
            ├── auth.js             # Sign-In/Sign-Up tab switcher & auth handlers
            ├── dashboard.js        # Recommendation cards, modal & roadmap UI logic
            ├── expert_call.js      # WebRTC peer connection & live chat stage engine
            ├── main.js             # Navigation controller & global announcement banner retriever
            └── upload.js           # File drag-and-drop & /analyze submission engine
```

---

## Getting Started

Follow these steps to set up and run CareerPulse locally.

### 1. System Prerequisites

Ensure you have the following installed:
- **Python 3.12+** (We recommend `uv`).
- **Node.js 20+** (For Tailwind CSS v4 and live server).
- **Tesseract-OCR**: Required for processing scanned image PDFs.
- **Poppler**: Required for 300 DPI PDF rasterization.

### 2. Backend Setup (Core Engine)

```bash
# 1. Configure environment variables
cp .env.example .env

# 2. Install Python dependencies and sync environment
uv sync

# 3. Launch the Backend Core Engine (runs on http://localhost:8000)
uv run uvicorn core_engine.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup & Execution

In a second terminal window:

```bash
cd web_interface
npm install
npm run build:css
npm run dev
# Starts Tailwind CSS watch mode and launches live-server on http://localhost:8080 (or :3000)
```

- **User Authentication**: Sign Up / Sign In via `login.html`.
- **Admin Control Console**: Access `admin.html` with credentials `admin@careerpulse.ai` / `admin123`.

### 4. Running Tests & Diagnostics

```bash
# Run full automated QA test suite
uv run python -m pytest quality_assurance/

# Check PyTorch CUDA & GPU status
uv run python quality_assurance/cuda_check.py
```

---

## Author & Developer

- **Mayank Anand**: Creator & Lead Engineer — System Architecture, Local Quantized LLM Inference, Embedded Vector Search, Document & OCR Extraction Engine, Web Presentation Layer, Authentication Subsystem, and Real-Time Telemetry.
