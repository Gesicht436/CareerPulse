# CareerPulse: Advanced Modular Architecture & Collaboration Guide

This document defines the system architecture, team responsibilities, and Git workflow for **CareerPulse**. We are building an industry-standard, adversarial-robust ATS simulator.

---

## 1. Team Distribution & Module Ownership

### 1.1 Core Engine (`core_engine/`)

**Owner:** **Mayank Anand (Team Lead)**

- **Tech Stack:** FastAPI (Async), Pydantic v2, spaCy, Sentence-Transformers, ChromaDB.
- **Responsibilities:**
- **API Gateway:** Secure REST endpoints, JWT authentication (if needed), and rate limiting.
- **Adversarial AI Defense:** Modules to detect "Resume Smuggling" (hidden text, zero-width chars, prompt injection).
- **Privacy Engine:** Client-side-first logic for PII redaction (Name, Email, Phone) before storage.
- **Smart Match Engine:** RAG-based semantic similarity between Resumes and JDs.
- **Data Layer:** PostgreSQL (via SQLModel) for user profiles and FAISS/ChromaDB for vector embeddings.

### 1.2 Web Interface (`web_interface/`)

**Primary:** **Member 3** | **Support:** **Member 4**

- **Tech Stack:** Next.js (App Router), TypeScript, Tailwind CSS, Lucide React, Shadcn/UI.
- **Responsibilities:**
- **Member 3 (Lead UI):** Component architecture, state management (Zustand/Context), and file upload logic.
- **Member 4 (Support):** Data visualization (D3.js or Recharts) for "Career Readiness" scores and skill-gap heatmaps.
- **Integration:** Connecting the frontend hooks to the `core_engine` API.

### 1.3 Data Pipeline (`data_pipeline/`)

**Owner:** **Member 2**

- **Tech Stack:** Python, BeautifulSoup4, Pandas.
- **Responsibilities:**
- **Scraping:** Gathering Job Descriptions and Resume datasets (Kaggle/Indeed).
- **Preprocessing:** Cleaning raw text, removing stop words, and formatting for spaCy entity recognition.
- **Taxonomy:** Maintaining a standardized "Skill Dictionary" used for gap analysis.

### 1.4 Quality Assurance (`quality_assurance/`)

**Owner:** **Member 4**

- **Tech Stack:** Pytest, Playwright (UI testing), Postman.
- **Responsibilities:**
- **Security Testing:** Crafting "adversarial" resumes to try and bypass Mayank's security logic.
- **Performance:** Benchmarking the latency of the embedding generation.
- **Coverage:** Ensuring core logic has >80% unit test coverage.

### 1.5 Project Assets (`project_assets/`)

**Owner:** **Member 2**

- **Responsibilities:**
- **Reporting:** Maintaining the Mid-sem and End-sem reports (Markdown/LaTeX).
- **Documentation:** API docs (Swagger/Redoc) and User Manuals.
- **Presentation:** Slide decks and demo recording assets.

---

## 2. Git & GitHub Workflow

To maintain code integrity, we will follow a strict **Feature Branch** workflow.

### 2.1 Branching Strategy

- `main`: **Protected.** Only stable, production-ready code.
- `develop`: Integration branch where all features meet.
- `feature/<module>-<desc>`: Individual task branches (e.g., `feature/core-pii-redaction`).

### 2.2 Contribution Rules

1. **Never commit directly to `main` or `develop`.**
2. **Pull Requests (PRs):** All PRs to `develop` must be reviewed by the Team Lead (Mayank).
3. **Commit Messages:** Follow conventional commits:
   - `feat: add adversarial detection logic`
   - `fix: resolve resume upload timeout`
   - `docs: update mid-sem report`

---

## 3. Communication Patterns

- **Frontend -> Backend:** All communication happens via the `/api/v1` prefix.
- **Backend -> Security:** The security module is a middleware that intercepts uploads.
- **Data Pipeline -> Core Engine:** Member 2 will provide `.jsonl` or `.csv` files that Mayank will ingest into the database/vector store.

---

## 4. Immediate Milestones (Deadline: March 30)

1. **Week 1:** Repo setup & Environment Config (Docker).
2. **Week 2:** Baseline Resume Parsing & Next.js UI Shell.
3. **Week 3:** Adversarial Detection Logic & Skill Gap Visualization.
4. **Week 4:** Integration testing & Report submission.
