# CareerPulse: System Architecture & Team Governance

This document serves as the master blueprint for the **CareerPulse** project. It details the high-level architecture, component interactions, data flow, and the rigorous work distribution among the development team. CareerPulse is built as a "Private AI" platform, designed to run sophisticated LLMs and Vector Search entirely on local infrastructure, ensuring 100% data sovereignty for job seekers.

---

## 1. High-Level Architecture

The system follows a **Modular Monolith** pattern, combining a robust FastAPI backend with a high-performance, utility-first frontend. This architecture ensures low latency for AI inference while maintaining a clear separation of concerns between security, data, and intelligence.

### A. Component Breakdown

1. **Web Interface (The Presentation Layer)**:
    - Built using HTML5, Vanilla JavaScript (ES6+), and **Tailwind CSS v4**.
    - Communicates with the backend via a centralized, environment-aware API client.
    - Handles complex data visualization for match scores and career roadmaps.

2. **FastAPI Core (The Orchestration Layer)**:
    - Manages the lifecycle of the application, including CORS policies and asynchronous routing.
    - Orchestrates the sequential flow from resume upload to final AI analysis.
    - Provides a unified `/analyze` endpoint that abstracts the complexity of the internal services.

3. **Security Service (The Defensive Layer)**:
    - Performs layout-preserved text extraction using `pdfplumber`.
    - Implements an OCR fallback pipeline (Tesseract + OpenCV) for scanned documents.
    - Executes **Named Entity Recognition (NER)** via spaCy for PII redaction.
    - Scans for adversarial "Prompt Injection" patterns and hidden text metadata.

4. **Smart Match Engine (The Intelligence Layer)**:
    - **Stage 1 (Vector Match)**: Uses `sentence-transformers` (all-MiniLM-L6-v2) to calculate semantic similarity scores via Cosine Distance.
    - **Stage 2 (Reasoning)**: Employs a local **Qwen 2.5 LLM** (quantized to 4-bit) to generate qualitative justifications, skill gaps, and learning roadmaps.

5. **Data Layer (The Persistence Layer)**:
    - Powered by **Qdrant**, a high-performance vector database.
    - Stores job descriptions as 384-dimensional vectors with rich metadata (payloads).
    - Utilizes HNSW indexing for sub-millisecond similarity retrieval.

---

## 2. Data Flow & Inference Pipeline

1. **Ingestion**: The user uploads a PDF. The `Web Interface` transmits it as `multipart/form-data`.
2. **Audit**: The `Security Service` extracts text, redacts personal identities, and verifies the "safeness" of the content.
3. **Retrieval**: The `Smart Match Engine` converts the redacted text into a vector and queries the `Data Layer` for the top 5 semantically similar job descriptions.
4. **Inference**: The `Local LLM` processes the top matches to generate expert career advice.
5. **Delivery**: The `FastAPI Core` bundles the security report and AI analysis into a single JSON response, which the `Web Interface` renders as a professional dashboard.

---

## 3. Team & Work Distribution

The project is led by **Mayank Anand**, who oversees the end-to-end integration and system integrity. The team is divided into specialized domains to ensure that every layer—from the database to the final UI polish—is handled with precision.

### Team Roles

- **Mayank Anand (Team Lead)**: System Architecture, API Integration Layer, Qdrant Configuration, Local LLM Inference Orchestration, Design Fine-tuning (Colors, Typography, Geometry), and Final Core Integration.
- **Abhinav Anand (285)**: Frontend Core Development, JavaScript State Management and Responsive Design Implementation.
- **Harsh Anand**: Frontend UI/UX Architecture, Component Structure, HTML/Tailwind Styling, and Responsive Design Implementation.
- **Abhinav Anand (08)**: Quality Assurance, Auditing Logic, Performance Benchmarking, and Automated Testing (Unit/Integration).
- **Ankit Anand**: Dataset Curation/Cleaning Security, Data Engineering, Data Ingestion Pipeline (ETL).

---

## 4. Work Assigned

This section tracks the specific tasks allocated to each team member. It serves as a living record of project expectations.

| Member | Assigned Task | Priority | Status |
| :--- | :--- | :--- | :--- |
| **Mayank Anand** | Configure Local LLM (Qwen 2.5) with 4-bit quantization and GPU acceleration. | Critical | Done |
| **Mayank Anand** | Fine-tune frontend aesthetics (border-radii, professional color palette, shadows). | Medium | Done |
| **Abhinav Anand (285)** | Build the JavaScript `apiClient` and integrate the `/analyze` and `/match` endpoints. | High | Done |
| **Abhinav Anand (285)** | Implement state management for the Analysis Dashboard and Career Roadmap. | High | Done |
| **Harsh Anand** | Design the HTML architecture for the Upload, Dashboard, and Search pages. | High | Done |
| **Harsh Anand** | Implement utility-first styling using Tailwind CSS v4 across all views. | High | Done |
| **Abhinav Anand (08)** | Develop unit tests for the `FastAPI backend` (redaction and injection checks). | Low | In process |
| **Abhinav Anand (08)** | Perform VRAM/Latency benchmarking for 1.5B vs 7B models. | Medium | In Process |
| **Ankit Anand** | Curate and clean the Tech Job Description dataset from Kaggle. | Medium | Pending |

---

## 5. Work Done

This section confirms the successfully completed and verified modules currently active in the project.

- **[Mayank Anand]**:
  - Architected the `core_engine` modular structure.
  - Integrated `sentence-transformers` for real-time vector generation.
  - Implemented the `LLMService` with `bitsandbytes` quantization.
  - Integrated Tailwind CSS v4 and optimized the build pipeline (`watch:css`).
  - Refined the `Web Interface` visuals (Professional blue-theme, rounded cards, smooth transitions).
- **[Abhinav Anand (285)]**:
  - Finalized the HTML layouts for `index.html`, `upload.html`, and `analyzer.html`.
  - Built the logic for `analyzer.js` and `dashboard.js` to parse AI JSON responses and `api.js` for centralized communication.
  - Ensured full responsiveness across mobile and desktop view.
- **[Harsh Anand]**:
  - Finalized the HTML layouts for `index.html`, `upload.html`, and `analyzer.html`.
  - Built the logic for `analyzer.js` and `dashboard.js` to parse AI JSON responses and `api.js` for centralized communication.
  - Ensured full responsiveness across mobile and desktop view.
- **[Abhinav Anand (08)]**:
  - Developed unit tests for the FastAPI backend.
- **[Ankit Annad]**:
  - Nothing until now

---

## 6. Hardware Compliance

The architecture is strictly bound by local hardware constraints:

- **Minimum VRAM**: 6GB (for 4-bit Qwen 1.5B).
- **Target VRAM**: 8GB+ (for 4-bit Qwen 7B).
- **Storage**: Qdrant indexed vectors require approx. 500MB per 100,000 jobs.
- **CPU Fallback**: System automatically switches to `cpu` if CUDA is unavailable, albeit with a 5-10x latency increase.
