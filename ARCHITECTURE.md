# CareerPulse: Advanced Modular Architecture & Collaboration Guide

This document defines the system architecture, team responsibilities, and Git workflow for **CareerPulse**. We are building an industry-standard, adversarial-robust ATS simulator.

---

## 1. Team Distribution & Module Ownership

### 1.1 Core Engine (`core_engine/`)

**Mayank Anand (Team Lead)** |

- **Tech Stack:** FastAPI, Uvicorn + Gunicorn, Pydantic v2, OAuth2 + JWT, Passlib, SlowAPI, Spacy, pdfplumber, regex + unicode normalization.
- **Responsibilities:**
- **API Gateway:** Secure REST endpoints, JWT authentication (if needed), and rate limiting.
- **Adversarial AI Defense:** Modules to detect "Resume Smuggling" (hidden text, zero-width chars, prompt injection).
- **Privacy Engine:** Client-side-first logic for PII redaction (Name, Email, Phone) before storage.
- **Smart Match Engine:** RAG-based semantic similarity between Resumes and JDs.
- **Data Layer:** Database for user profiles and vector embeddings.

### 1.2 Web Interface (`web_interface/`)

**Abhinav 285** | **Harsh** |

- **Tech Stack:** NextJS, Typescript, Tailwind CSS, Zustand(state management), React Hook Form + Zod, Recharts or ECharts.
- **Responsibilities:**
- **Abhinav 285:** Component architecture, state management, and file upload logic.
- **Harsh:** Data visualization for "Career Readiness" scores and skill-gap heatmaps.
- **Integration:** Connecting the frontend hooks to the `core_engine` API.

### 1.3 Data Pipeline (`data_pipeline/`)

**Mayank** | **Ankit**

- **Tech Stack:** Scrapy, Pandas, spaCy, NLTK, Prefect, PostgresSQL + Qdrant.
- **Responsibilities:**
- **Scraping:** Gathering Job Descriptions and Resume datasets (Kaggle/Indeed).
- **Preprocessing:** Cleaning raw text, removing stop words, and formatting for spaCy entity recognition.
- **Taxonomy:** Maintaining a standardized "Skill Dictionary" used for gap analysis.

### 1.4 Quality Assurance (`quality_assurance/`)

**Abhinav 08** |

- **Tech Stack:** Pytest, pytest-cov, Hypothesis, Postman + Newman, Atheris, Locust.
- **Responsibilities:**
- **Security Testing:** Crafting "adversarial" resumes to try and bypass Mayank's security logic.
- **Performance:** Benchmarking the latency of the embedding generation.
- **Coverage:** Ensuring core logic has >80% unit test coverage.

### 1.5 Project Assets (`project_assets/`)

**Mayank** | **Harsh** | **Ankit** | **Abhinav 08** | **Abhinav 285** |

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
