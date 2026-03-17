# CareerPulse

## The Adversarial-Robust ATS Simulator & Market Analyzer

CareerPulse isn't just another resume matcher. It's a high-stakes, security-first platform designed to bridge the gap between job seekers and roles while defending against the next generation of AI-driven manipulation.

Built for the Capstone Project at IIT Patna (2026).

---

## Core Value Proposition

- **Security First:** Client-side PII redaction and "Resume Smuggler" detection (Adversarial AI/Prompt Injection).
- **Smart Matching:** Context-aware RAG (Retrieval Augmented Generation) using Vector Embeddings, not just keyword density.
- **Explainable AI:** Provides a breakdown of matched skills, missing competencies, and learning paths.

---

## The Tech Stack

- **Frontend:** Next.js 15+ (App Router), TypeScript, Tailwind CSS v4, shadcn/ui, Zustand.
- **Backend:** FastAPI, Python 3.12 (managed via `uv`), Pydantic v2, pdfplumber, spaCy.
- **AI/ML:** Sentence-Transformers, Qdrant (Vector DB), en_core_web_sm (spaCy model).
- **Infrastructure:** Docker & Docker Compose, `uv` (Package Management).

---

## Current Progress

### Phase 1: Foundation, Security & Smart Match (In Progress)

- [ ] **Frontend Initialization:** Next.js project setup with Atomic Architecture.
- [ ] **UI/UX:** Responsive landing page, secure upload zone, and dashboard placeholder.
- [ ] **Backend Security:** Implementation of `Resume Security` module (PII detection, hidden text check).
- [ ] **Integration:** Frontend-to-Backend file upload pipeline established.
- [ ] **Smart Match (RAG):** Full integration with Qdrant Vector DB for semantic job retrieval.
- [ ] **Explainable AI:** Local LLM (`Qwen2.5-1.5B`) integrated for natural language feedback.
- [ ] **Career Roadmap:** Automated generation of detailed learning paths.

---

## Project Structure

The project is divided into 5 independent modules to ensure scalability and clear work distribution:

```text
C:\Users\mayan\coding\projects\CareerPulse
├── core_engine/        # Mayank - API, Security Logic, RAG, & DB Models
├── web_interface/      # Harsh & Abhinav 285 - Frontend & Visualizations
├── data_pipeline/      # Ankit - Scraping & Preprocessing scripts
├── quality_assurance/  # Abhinav 08 - Security Benchmarks & Testing
├── project_assets/     # Each member - Reports & Documentation
└── ARCHITECTURE.md     # Detailed Technical Specs & Git Workflow
```

---

## Getting Started

### 1. Prerequisites

- [uv](https://docs.astral.sh/uv/) (Modern Python package manager)
- Docker & Docker Compose
- Python
- Node.js
- cuda 13.0
- pytorch with cuda enabled

### 2. Environment Setup

```bash
# First install cuda 13.0

# Clone the repository
git clone https://github.com/Gesicht436/CareerPulse.git 
cd CareerPulse

# Initialize venv
uv venv venv
.venv\Scripts\Activate.ps1

# Install pytorch 
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130

# Sync dependencies
uv sync

# Setup Kaggle API Token
# a. Go to https://www.kaggle.com/settings -> API Section -> Create New API Token.
# b. This downloads 'kaggle.json'. Open it to find your 'username' and 'key'.
# c. Rename .env.example to .env:
# d. Edit .env and set KAGGLE_API_TOKEN using the format "username:key":
# KAGGLE_API_TOKEN="your_username:your_api_key_here"

# Download Project Datasets
# This script automatically fetches and unzips datasets into the correct folders
uv run python scripts/setup_data.py
```

### 3. Module Specific Setup

#### Backend (Core Engine)

```bash
uv run uvicorn core_engine.main:app --reload
```

#### Frontend (Web Interface)

```bash
cd ../web_interface
npm install
npm run dev
```

### 3. Running the Project

The easiest way is to use Docker:

```bash
docker-compose up --build
```

---

## Contribution Guidelines

We use a strict **Feature Branch** workflow.

1. **Branch Name:** `feature/<module>-<description>` (e.g., `feature/core-adversarial-detection`).
2. **Pull Requests:** Must be reviewed and approved by the Team Lead (Mayank).
3. **Commit Messages:** Follow [Conventional Commits](https://www.conventionalcommits.org/).
