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

- **Frontend:** NextJS, Typescript, Tailwind CSS, Zustand(state management), React Hook Form + Zod, Recharts or ECharts.
- **Backend:** FastAPI, Uvicorn + Gunicorn, Pydantic v2, OAuth2 + JWT, Passlib, SlowAPI, pdfplumber, regex + unicode normalization.
- **AI/ML:** Sentence-Transformers (`all-MiniLM-L6-v2`), Qdrant (Vector DB), Local LLMs (Qwen3 8B, GPTOSS), spaCy (Entity Recognition).
- **Infrastructure:** Docker containers, `uv` (Package Management).

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

### 2. Environment Setup

```bash
# Clone the repository
git clone https://github.com/Gesicht436/CareerPulse.git 
cd CareerPulse

# 1. Sync dependencies (Automatically creates .venv)
uv sync

# 2. Setup Kaggle API Token
# Rename .env.example to .env and paste your token
# Get your token from https://www.kaggle.com/settings (API section)
cp .env.example .env

# 3. Download Project Datasets
# This command automatically fetches the required Kaggle datasets
uv run download-data
```

### 3. Module Specific Setup

#### Backend (Core Engine)

```bash
cd core_engine
# (uv already handled dependencies in the root)
uv run uvicorn main:app --reload
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
