# CareerPulse: AI-Powered Career Optimization & Semantic Job Matching

**CareerPulse** is a modern, UX-first career intelligence platform that leverages local Large Language Models (LLMs), Vector Databases, and real-time interaction systems to provide job seekers with deep, actionable insights into their professional alignment. Unlike traditional ATS systems that rely on rigid keyword matching, CareerPulse understands the **semantic context** of your experience, reconstructing complex resume layouts, identifying skill gaps, and generating personalized learning roadmaps alongside live expert guidance, secure user accounts, and administrative site management controls.

---

## Core Value Proposition

CareerPulse delivers five foundational pillars:

1. **User Authentication & Session Persistence**: Secure Sign-In and Sign-Up authentication powered by PBKDF2 password hashing (100,000 iterations) and 7-day HMAC JWT tokens.
2. **UX-First Telemetry & Admin Control Console**: Captures real-time candidate alignment telemetry, platform usage counters (Users, Resumes Parsed, WebRTC Calls, Job Searches), system hardware stats (CPU, RAM, Uptime), activity audit logs, live announcement banner publishing, and instant feature flag toggles (`admin@careerpulse.ai`).
3. **Semantic-First Alignment & Top 5 Recommendations**: Powered by **SBERT (Sentence-BERT)** and Section-Aware Weighted Vector Search ($0.40 \times \text{Headline} + 0.60 \times \text{Body}$), the engine computes top 5 matched job recommendations across a 1.6M row job database with full job description inspection modals (`#job-inspect-modal`).
4. **Educational Qualification Degree Filtering**: Extracts degree qualifications (`B.Tech`, `M.Tech`, `B.Sc`, `M.Sc`, `BCA`, `MCA`, `B.Com`, `MBA`, `Ph.D`) directly from resume text and applies degree group filtering with an interactive dashboard filter toggle button (**"Disable Qualification Filter"** / **"Enable Qualification Filter"**).
5. **High-Fidelity Document & Video Intelligence**: Features a specialized PDF parsing engine that reconstructs multi-column layouts, extracts embedded tables/hyperlinks, and executes a 300 DPI dual-pass preprocessed OCR fallback (CLAHE + Adaptive Thresholding). Integrates native 1-on-1 WebRTC peer-to-peer video sessions for expert mentoring.

---

## Unified Technical Stack

The project is architected as a high-performance **Modular Monolith**, split between a specialized AI backend and a modern, utility-first frontend.

### **Backend (Core Engine)**

- **API Framework**: FastAPI (Asynchronous Python 3.12)
- **Authentication & Admin Control**: PBKDF2-HMAC-SHA256 password hashing, HMAC-SHA256 JWT tokens, Admin Router (`/api/v1/admin`)
- **Vector Intelligence**: Qdrant (High-performance HNSW indexing) & PyTorch Cached Tensor Matrix (`dataset_embeddings_cache.pt`)
- **Embedding Model**: `all-MiniLM-L6-v2` (384-dimensional semantic vectors)
- **Local LLM**: Qwen 2.5 1.5B/7B (Quantized via `bitsandbytes` NF4 4-bit)
- **Document & OCR Engine**: `pdfplumber`, `pdf2image`, `pytesseract` (300 DPI, `--psm 3`), `OpenCV` (CLAHE & Adaptive Thresholding)
- **Real-Time Communications**: Native FastAPI WebSockets & Custom WebRTC P2P Engine

### **Frontend (Web Interface)**

- **Styling**: Tailwind CSS v4 (Utility-first, optimized build pipeline)
- **Logic**: Vanilla ES6+ JavaScript (Zero-dependency, high-speed execution)
- **Architecture**: Static-site generation with dynamic API orchestration, top 5 recommendation cards, full job description inspection modal, interactive qualification toggle button, and Admin Control Portal (`admin.html`).

### **Automation & Ops**

- **Dependency Management**: `uv` (Fastest Python package manager)
- **Visualization**: `matplotlib`, `numpy` (Programmatic technical diagrams)
- **Documentation**: `pandoc` (Cross-format conversion)

---

## Current Project Status

| Milestone | Feature | Status |
| :--- | :--- | :--- |
| **Authentication** | Sign-In & Sign-Up system (PBKDF2, JWT tokens, user DB) | [x] Completed |
| **Admin Control** | Admin portal (`admin.html`), telemetry metrics, audit logs, feature flags | [x] Completed |
| **Document Processing** | Multi-column layout reconstruction, Table & Hyperlink harvesting | [x] Completed |
| **OCR Intelligence** | 300 DPI Dual-Pass Preprocessed OCR (CLAHE + Adaptive Thresholding) | [x] Completed |
| **Data Layer** | Qdrant Vector DB & Cached PyTorch Tensor Matrix (`(5000, 384)`) | [x] Completed |
| **Matching Engine** | Top 5 Job Recommendations, SBERT Section-Aware Scoring & Token-Aware Skill Matcher | [x] Completed |
| **Degree Filtering** | Automatic Degree Extraction (`B.Tech`, `B.Sc`, etc.) & Interactive Dashboard Filter Toggle | [x] Completed |
| **Job Inspection** | Full Job Description Inspection Modal (`#job-inspect-modal`) & Action Links | [x] Completed |
| **Intelligence** | Local LLM Integration (Qwen 2.5) with 4-bit quantization | [x] Completed |
| **Expert System** | WebRTC 1-on-1 Peer-to-Peer Live Video & AI Briefing Dossier | [x] Completed |
| **Web UI** | Responsive Dashboard, Upload Hub, Job Search, Admin Hub & Live Stage | [x] Completed |
| **Orchestration** | Unified End-to-End Analysis Pipeline (`/api/v1/analyze`) | [x] Completed |

---

## Project Structure

```text
CareerPulse/
├── core_engine/                # Backend Central Nervous System
│   ├── admin/                  # Admin authentication & site settings control router
│   ├── auth/                   # Sign-In/Sign-Up subsystem (PBKDF2 & JWT tokens)
│   ├── data_layer/             # Dataset vector retrieval & degree filtering service
│   ├── datasets/               # 1.6M row job dataset (job_descriptions.csv) & PyTorch cache
│   ├── resume_security/        # Optimized High-Fidelity PDF & OCR Extraction Engine
│   ├── smart_match/            # SBERT Scoring, Token-Aware Skill Matcher & Qwen 2.5 LLM
│   ├── telemetry/              # Real-time telemetry logging service & activity audit feed
│   ├── expert_session/         # WebRTC Signaling Hub & AI Briefing Dossier
│   ├── embedding_service.py    # Shared SBERT singleton
│   ├── llm_service.py          # Local Qwen 2.5 4-bit inference layer
│   └── main.py                 # FastAPI Gateway & unified routes
├── web_interface/              # Modern Professional Frontend
│   ├── public/                 # HTML templates & static assets
│   │   ├── css/                # Tailwind v4 source & output
│   │   ├── js/                 # Vanilla JS logic (main.js, admin.js, upload.js, dashboard.js, expert_call.js)
│   │   └── admin.html          # Admin Control Console & Telemetry Hub
│   └── package.json            # Node.js build scripts
├── scripts/                    # Automation & Data Pipelines
│   ├── ingest_qdrant.py        # Vector ETL pipeline
│   ├── setup_data.py           # Automated Kaggle data retrieval
│   └── generate_visuals.py     # Technical diagram generator
├── quality_assurance/          # QA Test Suite (test_auth.py, test_main.py, test_smart_match.py)
├── ARCHITECTURE.md             # Master system blueprint
├── USER_FEATURES.md            # Comprehensive user feature catalog
└── README.md                   # Primary project readme
```

---

## Getting Started

Follow these steps to set up the complete CareerPulse environment on your local machine.

### 1. System Prerequisites

Ensure you have the following system-level dependencies installed:

- **Python 3.12+** (We recommend the `uv` package manager).
- **Node.js 20+** (For frontend styling & build scripts).
- **Tesseract-OCR**: Required for processing scanned PDFs.
- **Poppler**: Required for PDF rasterization.
- **Docker**: Optional, to run the Qdrant vector database container.

```bash
winget install --id Nvidia.CUDA --version 13.0
winget install Docker.DockerDesktop
uv install python 3.12
winget install CoreyButler.NVMforWindows
nvm install latest
```

### 2. Backend Setup (Core Engine)

```bash
# 1. Configure environment variables
cp .env.example .env

# 2. Install Python dependencies and sync environment
uv sync
```

### 3. Launch the Engine

```bash
uv run uvicorn core_engine.main:app --reload --port 8000
```

### 4. Frontend Setup & Execution

In a new terminal window:

```bash
cd web_interface
npm install
npm run build:css
npm run dev
```

Your application will be live at `http://localhost:3000`, communicating with the backend at `http://localhost:8000`.

- **User Authentication**: Sign Up / Sign In via `login.html`.
- **Admin Control Console**: Access `admin.html` with credentials `admin@careerpulse.ai` / `admin123`.

---

## Author & Solo Developer

- **Mayank Anand**: Creator & Lead Engineer — System Architecture, Local LLM Inference, Embedded Vector Search, Document Extraction, Web Interface, Auth Subsystem, and Telemetry Engine.
