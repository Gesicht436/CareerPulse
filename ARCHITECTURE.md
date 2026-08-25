# CareerPulse: System Architecture & Technical Specifications

This document serves as the master architectural blueprint for the **CareerPulse** project. It details the high-level system design, component interactions, data flow, and technical implementation. CareerPulse is engineered as a modern, UX-first local AI platform that combines high-performance LLMs, 1.61M vector embedding ranking, high-fidelity PDF extraction, 1-on-1 WebRTC video stages, secure user authentication, and administrative site control console.

---

## 1. High-Level Architecture

The system follows a **Modular Monolith** pattern, combining a robust FastAPI backend with a high-performance, utility-first frontend. This architecture ensures sub-second latency for AI inference while maintaining clear subsystem separation between user authentication, admin control, document extraction, vector persistence, AI reasoning, and real-time WebRTC communications.

### A. Component Breakdown

1. **Web Interface (The Presentation Layer)**:
    - Built using HTML5, Vanilla JavaScript (ES6+), and **Tailwind CSS v4**.
    - Communicates with the backend via a centralized, environment-aware API client (`api.js`) with automatic Bearer Token attachment.
    - Renders dynamic dashboards, top 5 recommendation cards, full job inspection modal (`#job-inspect-modal` with company profile, portal source, responsibilities), interactive qualification filter toggle control, live 1-on-1 WebRTC stages, Sign-In / Sign-Up auth hubs (`login.html`), and Admin Control Console (`admin.html`).

2. **FastAPI Core (The Orchestration Layer)**:
    - Manages application lifecycle, CORS policies, and asynchronous routing.
    - Exposes the unified `/api/v1/analyze` gateway alongside modular subsystem endpoints (`/auth`, `/admin`, `/security`, `/smart-match`, `/expert`).

3. **Document & Preprocessed OCR Engine (`core_engine/resume_security`)**:
    - High-fidelity PDF parsing utilizing `pdfplumber` layout-aware text extraction and spatial coordinate sorting (`top, x0`).
    - Table cell extraction and embedded hyperlink harvesting (`page.hyperlinks` / `page.annots`).
    - 300 DPI dual-pass preprocessed OCR fallback (`pdf2image` + OpenCV CLAHE + Bilateral Noise Filter + Adaptive Gaussian Thresholding + `pytesseract` `--psm 3`).

4. **1.61M Single-Tier Vector Matrix & SQLite Engine (`core_engine/data_layer`)**:
    - Embedded SQLite database (`jobs.db`, 1.78 GB in WAL mode) storing 18 structured job fields. Zero external Docker containers or vector databases required.
    - In-memory PyTorch FP16 tensor matrix (`embeddings/dataset_embeddings_full.pt`, shape `(1615940, 384)`, ~1.24 GB) + degree bitmask tensor (`embeddings/dataset_meta_full.pt`) providing **~200 ms** warm vector discovery across all 1,615,940 jobs.

5. **Smart Matcher & Local LLM Service (`core_engine/smart_match` & `llm_service.py`)**:
    - Sentence-BERT (`all-MiniLM-L6-v2`) section-aware similarity calculation ($0.40 \times \text{Headline} + 0.60 \times \text{Body}$).
    - Educational qualification degree group filter (`DEGREE_GROUPS` / `DEGREE_CODE_MAP`).
    - Token-aware technical skill matcher (`is_skill_in_text`) against 150+ technical terms.
    - Local **Qwen 2.5** instruction-tuned model (`1.5B`/`7B`) quantized using `bitsandbytes` 4-bit NormalFloat4 (NF4) for structured JSON advice and weekly roadmaps.

6. **WebRTC Signaling & AI Briefing Subsystem (`core_engine/expert_session`)**:
    - Native FastAPI WebSocket signaling hub (`/api/v1/expert/ws/{room_id}`) handling P2P WebRTC session negotiation (`offer`, `answer`, `ice_candidate`, `chat_message`, `hangup`).
    - Automated AI Expert Briefing Dossier synthesis summarizing candidate match scores, security status, and skill gaps for mentors.

7. **Admin Control Console & Real-Time Telemetry Engine (`core_engine/admin` & `core_engine/telemetry`)**:
    - Real-time hardware telemetry (`psutil` CPU %, RAM %, Uptime) and activity counters (Page Views, Resumes Parsed, WebRTC Calls, Job Searches).
    - Global site settings publisher (live announcement banner, maintenance mode toggle, feature flags).

---

## 2. End-to-End Execution & Data Flow

```text
[User Browser] ---> (POST /api/v1/analyze) ---> [FastAPI Gateway main.py]
                                                          │
   ┌──────────────────────────────────────────────────────┴──────────────────────────────────────────────────────┐
   ▼                                                      ▼                                                      ▼
[SecurityService]                                [DataLayerService]                                     [SmartMatchService]
 Spatial PDF & OCR                              1.61M PyTorch Vector Matrix                            SBERT Vector Ranking
 Text Extraction                                 + SQLite WAL Storage                                  + Token Skill Matcher
   │                                                      │                                                      │
   └──────────────────────────────────────────────────────┼──────────────────────────────────────────────────────┘
                                                          ▼
                                                  [LLMService Qwen 2.5]
                                                   4-bit Quantized Advice
                                                          │
                                                          ▼
                                            [JSON Response to Browser]
                                        Cards, Ring, Inspection Modal, Roadmap
```

1. **Client Request**: Candidate uploads resume PDF via `upload.html` or `upload.js` sending `Multipart/form-data` with Bearer token header.
2. **Ingestion & Extraction**: `SecurityService` performs spatial multi-column layout reconstruction, hyperlink harvesting, hyphen normalization, and preprocessed dual-pass OCR.
3. **Degree & Qualification Extraction**: `main.py` parses candidate degree (`B.Tech`, `B.Sc`, `MBA`, etc.). `DataLayerService` applies GPU degree bitmask filtering.
4. **Retrieval**: `DataLayerService` embeds extracted text via `EmbeddingService` (`all-MiniLM-L6-v2`) and performs section-aware vector search across the 1.61M PyTorch tensor matrix, retrieving winning records from SQLite in **~200 ms**.
5. **Skill Evaluation & LLM Inference**: `SmartMatchService` token-matches technical skills, calibrates ATS score (50% vector + 50% skill overlap), and queries `LLMService` (local 4-bit Qwen 2.5) to generate structured JSON advice.
6. **Delivery & UX Telemetry**: `main.py` returns top 5 recommendations and logs telemetry events. `dashboard.js` renders recommendation cards, score ring, inspection modal, and roadmap.

---

## 3. Project Ownership & Development

**CareerPulse** is designed, engineered, and maintained independently by **Mayank Anand** as a solo developer, encompassing end-to-end system architecture, AI inference pipelines, vector search, document parsing, user authentication, telemetry analytics, and web presentation layer.

### System Responsibilities Implemented by Mayank Anand:
- **Core Engine Architecture**: FastAPI Application Gateway, async routing, middleware, and CORS configuration.
- **Authentication & Admin Subsystem**: PBKDF2 password hashing (100,000 iterations), HMAC-SHA256 JWT tokens, persistent user DB, and Admin Control Console API (`/api/v1/admin`).
- **Real-Time Telemetry Engine**: `psutil` system metrics integration, activity audit feed, metric logging, and live announcement banner publisher.
- **Document & Preprocessed OCR Engine**: Layout-aware `pdfplumber` parsing, spatial word reconstruction, table/hyperlink harvesting, and 300 DPI dual-pass CLAHE OCR fallback.
- **1.61M Single-Tier Data Layer & PyTorch Matrix**: SQLite job metadata storage (`jobs.db`, 1.78 GB in WAL mode) and 1.61M PyTorch FP16 vector matrix (`embeddings/dataset_embeddings_full.pt`, 1.24 GB).
- **Matching & LLM Inference Layer**: SBERT section-aware cosine ranking, token-aware skill matcher (`is_skill_in_text`), and local quantized Qwen 2.5 4-bit NF4 instruction LLM pipeline.
- **Real-Time WebRTC Stage**: Native FastAPI WebSocket signaling hub (`/api/v1/expert/ws/{room_id}`) and AI Expert Briefing Dossier generator.
- **Web Presentation Layer**: Full HTML5, Tailwind CSS v4, and Vanilla ES6+ JS interface (`web_interface/public`).
- **Quality Assurance & Testing**: Unit test suite (`quality_assurance/`) covering auth, gateway routes, and matching logic.

---

## 4. Hardware & Runtime Specifications

- **Minimum VRAM**: 6GB (Runs PyTorch FP16 matrix search and 4-bit Qwen 1.5B).
- **Target VRAM**: 8GB+ (for 4-bit Qwen 7B).
- **Storage**:
  - `jobs.db`: 1.78 GB (SQLite database with 1.61M rows).
  - `embeddings/dataset_embeddings_full.pt`: 1.24 GB (PyTorch FP16 tensor matrix).
  - `embeddings/dataset_meta_full.pt`: 43 MB (metadata and degree bitmasks).
- **CPU Fallback**: System automatically switches to `cpu` if CUDA is unavailable.
