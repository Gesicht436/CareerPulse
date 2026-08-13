# CareerPulse: Complete User Feature Guide & Catalog

Welcome to the comprehensive feature catalog for **CareerPulse**, a UX-first local AI career intelligence platform, ATS simulator, and site administration environment.

This document details every feature available to job seekers, developers, system administrators, and career advisors using CareerPulse—covering user authentication, admin control portals, user interface elements, backend intelligence services, high-fidelity document parsing, real-time WebRTC expert calls, and career optimization tools.

---

## 1. Executive Summary & Value Pillars

CareerPulse empowers job seekers and platform administrators with deep, actionable career insights and real-time site control by combining secure user accounts, high-fidelity document parsing, local semantic AI analysis, admin telemetry logging, and live expert mentoring.

### Core Value Pillars

- **User Authentication & Account Management**: Secure user registration and login with PBKDF2 password hashing (100,000 iterations) and 7-day HMAC-SHA256 JWT tokens.
- **Admin Control Console & Telemetry Analytics**: Real-time site management portal (`admin.html`) featuring usage counters (Users, Resumes, Calls, Searches, Page Views), hardware load tracking (CPU, RAM, Uptime), live activity audit feed, global top announcement banner publisher, and instant feature flag toggles (`admin@careerpulse.ai`).
- **Semantic-First Alignment & Top 5 Recommendations**: Powered by **SBERT (Sentence-BERT)** and Section-Aware Weighted Vector Search ($0.40 \times \text{Headline} + 0.60 \times \text{Body}$), the engine computes top 5 matched job recommendations across a 1.6M row job database with full job description inspection modals (`#job-inspect-modal`).
- **Educational Qualification Degree Filtering**: Extracts degree qualifications (`B.Tech`, `M.Tech`, `B.Sc`, `M.Sc`, `BCA`, `MCA`, `B.Com`, `MBA`, `Ph.D`) directly from resume text and applies degree group filtering with an interactive dashboard filter toggle button (**"Disable Qualification Filter"** / **"Enable Qualification Filter"**).
- **High-Fidelity Document Extraction**: Features spatial multi-column layout reconstruction, borderless table parsing, hyperlink target harvesting, hyphen normalization, and 300 DPI dual-pass preprocessed OCR (CLAHE + Adaptive Thresholding).
- **Live Expert Mentoring Stage**: Features native WebRTC peer-to-peer audio/video calling coupled with automated AI Expert Briefing Dossiers.

---

## 2. Comprehensive User Feature Catalog

### 1. User Sign-In & Sign-Up Authentication Hub

- **Location**: [`web_interface/public/login.html`](file:///C:/Users/mayan/Development/Projects/CareerPulse/web_interface/public/login.html)
- **Script**: [`web_interface/public/js/auth.js`](file:///C:/Users/mayan/Development/Projects/CareerPulse/web_interface/public/js/auth.js)
- **Backend Module**: [`core_engine/auth/service.py`](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/auth/service.py) & `router.py`
- **API Endpoints**: `POST /api/v1/auth/signup`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me`
- **Description**: Secure authentication hub allowing job seekers to register accounts, log in securely, and manage persistent session tokens.
- **Key Capabilities**:
  - **Interactive Tab Switcher**: Smooth tab navigation between **Sign In** and **Sign Up** forms.
  - **PBKDF2 Password Security**: Hashes user passwords using PBKDF2-HMAC-SHA256 with 100,000 iterations and unique 16-byte random salts.
  - **JWT Session Authorization**: Issues signed 7-day HMAC-SHA256 access tokens (`auth_token`) stored in `localStorage` and attached via `Authorization: Bearer <token>` to all API requests.

---

### 2. Admin Control Console & Telemetry Hub

- **Location**: [`web_interface/public/admin.html`](file:///C:/Users/mayan/Development/Projects/CareerPulse/web_interface/public/admin.html)
- **Script**: [`web_interface/public/js/admin.js`](file:///C:/Users/mayan/Development/Projects/CareerPulse/web_interface/public/js/admin.js)
- **Backend Module**: [`core_engine/admin/router.py`](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/admin/router.py) & [`core_engine/telemetry/service.py`](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/telemetry/service.py)
- **API Endpoints**: `POST /api/v1/admin/login`, `GET /api/v1/admin/telemetry`, `POST /api/v1/admin/settings`, `GET /api/v1/admin/users`, `DELETE /api/v1/admin/users/{id}`
- **Description**: Master administrative control hub for site administrators (`admin@careerpulse.ai` / `admin123`).
- **Key Capabilities**:
  - **Telemetry Dashboard**: Real-time display of total users, resumes analyzed, WebRTC mentorship calls, vector searches, page views, and system CPU/RAM/Uptime stats.
  - **Live Announcement Banner Publisher**: Edit and publish global top notification banners rendered dynamically across all public site pages via `main.js`.
  - **Instant Feature Flags**: Enable/disable WebRTC calls, resume uploads, JD analyzer, or toggle site maintenance mode in real time.
  - **Candidate User Management**: Inspect registered users and execute one-click user deletions.
  - **Activity Audit Feed**: Real-time event log stream tracking user activity with color-coded badges.

---

### 3. Resume Upload Hub & Multi-Format Ingestion

- **Location**: [`web_interface/public/upload.html`](file:///C:/Users/mayan/Development/Projects/CareerPulse/web_interface/public/upload.html)
- **Script**: [`web_interface/public/js/upload.js`](file:///C:/Users/mayan/Development/Projects/CareerPulse/web_interface/public/js/upload.js)
- **Description**: Primary entry point for job seekers to ingest their resume into the system.
- **Key Capabilities**:
  - **Drag-and-Drop Interface**: Intuitive file drop zone with visual drag state feedback.
  - **Simulated Real-Time Progress Bar**: Provides live visual feedback while backend processes vector extraction and local LLM inference.
  - **Automatic Session Persistence**: Stores full analysis results in `localStorage` (`latest_analysis`) for client-side navigation to the analysis dashboard.

---

### 4. High-Fidelity Document & Dual-Pass Preprocessed OCR Extraction Engine

- **Backend Module**: [`core_engine/resume_security/service.py`](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/resume_security/service.py)
- **API Endpoint**: `POST /api/v1/security/upload` & `POST /api/v1/analyze`
- **Description**: High-performance PDF extraction engine optimizing vector text parsing, multi-column layouts, tabular structures, embedded URLs, and scanned image OCR.
- **Key Capabilities**:
  - **Spatial Multi-Column Reconstruction**: Uses word coordinate sorting (`top, x0`) in `pdfplumber` to reconstruct multi-column layouts cleanly.
  - **Structured Table & Hyperlink Parsing**: Parses borderless grid tables and extracts target URIs (`page.hyperlinks` / `page.annots`) for GitHub, LinkedIn, and personal portfolio links.
  - **Line-Wrap Hyphen Normalization**: Automatically repairs line-wrapped words (`Py-\nthon` $\to$ `Python`).
  - **300 DPI Preprocessed Dual-Pass OCR**: Rasterizes scanned pages at `300 DPI` via `pdf2image` and applies OpenCV CLAHE contrast enhancement, bilateral noise filtering, and adaptive Gaussian thresholding. Executes dual-pass Tesseract OCR (`--psm 3`).

---

### 5. Top 5 Job Recommendations & Dynamic Vector Search Engine

- **Backend Module**: [`core_engine/smart_match/service.py`](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/smart_match/service.py) & [`core_engine/data_layer/service.py`](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/data_layer/service.py)
- **API Endpoint**: `POST /api/v1/analyze` & `POST /api/v1/smart-match/match`
- **Description**: Core intelligence subsystem calculating top 5 matched job recommendations from a 1.6M row job database.
- **Key Capabilities**:
  - **Section-Aware Weighted Vector Search**: Computes 384-dimensional SBERT embeddings with hybrid weighting ($0.40 \times \text{Headline} + 0.60 \times \text{Body}$).
  - **Token-Aware Skill Matcher (`is_skill_in_text`)**: Tokenizes skill phrases and matches core technical terms against candidate resume text using a built-in 150+ tech dictionary.
  - **Pre-Computed Tensor Cache Matrix**: Loads pre-computed dataset embeddings tensor (`dataset_embeddings_cache.pt`) in $< 10\text{ms}$.
  - **Multi-Factor ATS Score Calibration**: Maps SBERT document cosine range $[0.12, 0.60]$ to $[0\%, 100\%]$ and blends 50% vector similarity + 50% technical skill overlap ratio.

---

### 6. Educational Qualification Degree Filtering Engine

- **Backend Module**: [`core_engine/data_layer/service.py`](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/data_layer/service.py)
- **Location**: [`web_interface/public/dashboard.html`](file:///C:/Users/mayan/Development/Projects/CareerPulse/web_interface/public/dashboard.html)
- **Description**: Automated degree extraction and qualification group filtering.
- **Key Capabilities**:
  - **Degree Extraction**: Automatically extracts degree qualifications (`B.Tech`, `M.Tech`, `B.Sc`, `M.Sc`, `BCA`, `MCA`, `B.Com`, `MBA`, `Ph.D`) from resume text.
  - **Strict Qualification Filter**: Restricts job recommendations to dataset postings matching candidate degree categories (`DEGREE_GROUPS`).
  - **Interactive Dashboard Toggle Button**: Users can toggle between **Strict Qualification Mode** (restricted to candidate's degree) and **All-Roles Mode** (showing overall top recommendations across all fields).

---

### 7. Interactive Analysis Dashboard & Job Inspection Modal

- **Location**: [`web_interface/public/dashboard.html`](file:///C:/Users/mayan/Development/Projects/CareerPulse/web_interface/public/dashboard.html)
- **Script**: [`web_interface/public/js/dashboard.js`](file:///C:/Users/mayan/Development/Projects/CareerPulse/web_interface/public/js/dashboard.js)
- **Description**: Visual dashboard displaying top 5 recommendation cards, radial ATS score ring, skill gap badges, score rationale, and full job description inspection modal.
- **Key Capabilities**:
  - **Top 5 Recommendation Cards**: Display rank tags (`#1 Match`, `#2 Match`), company names, locations, and match score badges.
  - **Click-to-Inspect Modal (`#job-inspect-modal`)**: Clicking **"Inspect →"** opens a modal displaying full Job Title, Company, Location, Experience Level, Salary Range, Qualifications, Full Job Description text, and matched/missing technical skills.
  - **Dynamic Analysis Switching**: Clicking any recommendation card dynamically updates the active dashboard score ring, skill gap badges, and roadmap.

---

### 8. AI-Generated Personalized Career Roadmap

- **Location**: [`web_interface/public/dashboard.html`](file:///C:/Users/mayan/Development/Projects/CareerPulse/web_interface/public/dashboard.html#roadmap-container)
- **Script**: [`web_interface/public/js/dashboard.js`](file:///C:/Users/mayan/Development/Projects/CareerPulse/web_interface/public/js/dashboard.js)
- **Description**: Week-by-week learning timeline generated by local Qwen 2.5 LLM to bridge skill gaps.

---

### 9. 1-on-1 Live Expert Mentoring Stage & AI Briefing Dossier

- **Location**: [`web_interface/public/expert_call.html`](file:///C:/Users/mayan/Development/Projects/CareerPulse/web_interface/public/expert_call.html)
- **Script**: [`web_interface/public/js/expert_call.js`](file:///C:/Users/mayan/Development/Projects/CareerPulse/web_interface/public/js/expert_call.js)
- **Backend Module**: [`core_engine/expert_session/service.py`](file:///C:/Users/mayan/Development/Projects/CareerPulse/core_engine/expert_session/service.py) & `router.py`
- **Description**: Real-time WebRTC peer-to-peer stage connecting candidates with industry experts.

---

## 3. Feature Availability & Interface Matrix

| Feature | UI Access Point | Backend Service / Module | User Objective |
| :--- | :--- | :--- | :--- |
| **Sign-In & Sign-Up Auth** | `login.html` | `core_engine/auth/router.py` | Create user account & manage session tokens |
| **Admin Control Portal** | `admin.html` | `core_engine/admin/router.py` | Telemetry analytics, banner publisher & feature flags |
| **PDF Resume Upload** | `upload.html` | `core_engine/main.py` (`/analyze`) | Ingest resume for complete ATS analysis |
| **Top 5 Job Recommendations**| `dashboard.html` | `smart_match/service.py` | View top 5 matched job postings |
| **Degree Filter Toggle** | `dashboard.html` | `data_layer/service.py` | Toggle qualification restriction on/off |
| **Job Description Modal** | `#job-inspect-modal` | `dashboard.js` | Inspect unabridged job description & skills |
| **Match Score Ring** | `dashboard.html` | `smart_match/service.py` | View overall semantic alignment percentage |
| **Skill Gap Analysis** | `dashboard.html` | `smart_match/service.py` + `llm_service.py` | Identify matched and missing technical skills |
| **Weekly Roadmap** | `dashboard.html` | `llm_service.py` | Follow structured step-by-step learning plan |
| **WebRTC 1-on-1 Expert Stage** | `expert_call.html` | `expert_session/router.py` | Connect with industry mentor via P2P video call |
| **Custom JD Analyzer** | `analyzer.html` | `smart_match/router.py` (`/match`) | Paste external JDs for instant evaluation |
| **Semantic Job Search**| `search.html` | `data_layer/service.py` (`/search-jobs`) | Search database by experience & natural query |
