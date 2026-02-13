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

- **Frontend:** Next.js (TypeScript) + Tailwind CSS + Lucide React.
- **Backend:** FastAPI (Python) - Async, Pydantic v2.
- **Database:** PostgreSQL (User data) + ChromaDB/FAISS (Vector Embeddings).
- **AI/ML:** LangChain, spaCy, HuggingFace Transformers.
- **Infrastructure:** Dockerized Containers.

---

## Project Structure

The project is divided into 5 independent modules to ensure scalability and clear work distribution:

```text
C:\Users\mayan\coding\projects\CareerPulse
├── core_engine/        # [MAYANK] API, Security Logic, RAG, & DB Models
├── web_interface/      # [MEMBERS 3 & 4] Next.js Frontend & Visualizations
├── data_pipeline/      # [MEMBER 2] Scraping & Preprocessing scripts
├── quality_assurance/  # [MEMBER 4] Security Benchmarks & Testing
├── project_assets/     # [MEMBER 2] Reports & Documentation
└── ARCHITECTURE.md     # Detailed Technical Specs & Git Workflow
```

---

## Getting Started

### 1. Prerequisites

- Docker & Docker Compose
- Python 3.10+
- Node.js 18+

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/your-org/CareerPulse.git
cd CareerPulse

# Setup Backend (Core Engine)
cd core_engine
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Setup Frontend (Web Interface)
cd ../web_interface
npm install
```

### 3. Running the Project

The easiest way is to use Docker:
```bash
docker-compose up --build
```
Alternatively, for development:
- **Backend:** `uvicorn main:app --reload` (inside `core_engine`)
- **Frontend:** `npm run dev` (inside `web_interface`)

---

## Contribution Guidelines

We use a strict **Feature Branch** workflow.

1. **Branch Name:** `feature/<module>-<description>` (e.g., `feature/core-adversarial-detection`).
2. **Pull Requests:** Must be reviewed and approved by the Team Lead (Mayank).
3. **Commit Messages:** Follow [Conventional Commits](https://www.conventionalcommits.org/).
