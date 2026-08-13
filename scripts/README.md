# CareerPulse Scripts: Automation & Data Pipelines

The `scripts/` directory contains the operational backbone of the CareerPulse project. These scripts handle everything from data acquisition and database initialization to the generation of professional technical visuals and documentation conversion.

## Script Directory Overview

| Script | Purpose | Key Dependencies |
| :--- | :--- | :--- |
| `setup_data.py` | Automated dataset acquisition from Kaggle | `kaggle`, `python-dotenv` |
| `ingest_qdrant.py` | Vector embedding and Qdrant ingestion | `qdrant-client`, `pandas`, `sentence-transformers` |
| `generate_visuals.py` | Generation of architectural and performance diagrams | `matplotlib`, `numpy` |
| `md_to_docs.py` | Professional Markdown to DOCX converter | `pypandoc`, `pandoc` |

---

## 1. Data Acquisition: `setup_data.py`

This script automates the retrieval of large-scale job description datasets required to power the semantic search engine.

### How it Works

1. **Authentication**: Loads `KAGGLE_API_TOKEN` from your `.env` file.
2. **Dataset Targeting**: Targets the `adityarajsrv/job-descriptions-2025-tech-and-non-tech-roles` dataset.
3. **Download & Extract**: Uses Kaggle API to download and extract the dataset into `core_engine/datasets/raw`.

### How to Run

```bash
uv run python scripts/setup_data.py
```

---

## 2. Vector Ingestion: `ingest_qdrant.py`

Transforms raw job text into 384-dimensional vectors and populates the **Qdrant Vector Database**.

### How it Works

1. **Data Cleaning**: Reads CSV dataset and cleans missing fields.
2. **Semantic Synthesis**: Combines Job Title, Skills, and Responsibilities into a single context string.
3. **Embedding Generation**: Passes context strings through `EmbeddingService` (`all-MiniLM-L6-v2`), generating **384-dimensional vectors**.
4. **Batch Upsert**: Uploads vectors and metadata payloads to Qdrant in batches of 100 points.

### How to Run

```bash
uv run python scripts/ingest_qdrant.py
```

---

## 3. Professional Visuals: `generate_visuals.py`

Generates high-resolution technical diagrams for documentation and system reports:

- **System Architecture**: High-level component diagrams.
- **Document Pipeline**: Step-by-step visualization of PDF extraction, table parsing, and OCR pipeline.
- **RAG Workflow**: Diagram showing Retrieval-Augmented Generation processes.
- **Performance Graphs**: VRAM usage and Latency comparisons between different LLM models.

### How to Run

```bash
uv run python scripts/generate_visuals.py
```

---

## 4. Documentation Converter: `md_to_docs.py`

Converts Markdown documentation files into styled Microsoft Word (.docx) documents using `pandoc`.

### How to Run

```bash
uv run python scripts/md_to_docs.py README.md -o Final_Report.docx
```
