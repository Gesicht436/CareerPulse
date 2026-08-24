# CareerPulse Scripts: Automation & Data Pipelines

The `scripts/` directory contains automation, data ingestion, documentation conversion, and technical visualization pipelines for **CareerPulse**.

---

## 1. Script Directory Overview

| Script | Purpose | Key Dependencies |
| :--- | :--- | :--- |
| `setup_data.py` | Automated dataset acquisition from Kaggle | `kaggle`, `python-dotenv` |
| `ingest_qdrant.py` | Dataset cleaning, SQLite database populator & PyTorch tensor matrix generator | `pandas`, `sqlite3`, `torch`, `sentence-transformers` |
| `generate_visuals.py` | Generation of architectural and performance diagrams | `matplotlib`, `numpy` |
| `md_to_docs.py` | Markdown to styled DOCX document converter | `pypandoc`, `pandoc` |

---

## 2. Script Details & Execution

### 1. Data Acquisition: `setup_data.py`
Automates retrieval of the 1.6M Kaggle job descriptions dataset required to populate the local database:
- **Authentication**: Loads `KAGGLE_API_TOKEN` / credentials from environment.
- **Target Dataset**: `adityarajsrv/job-descriptions-2025-tech-and-non-tech-roles`.
- **Destination**: Downloads and extracts archive into `core_engine/datasets/raw/job_descriptions.csv`.

```bash
uv run python scripts/setup_data.py
```

### 2. Dataset Ingestion & Tensor Cache: `ingest_qdrant.py`
Transforms raw job postings into structured SQLite records and pre-computes normalized 384D SBERT vector embeddings:
- **Data Cleaning**: Strips missing values and normalizes job fields.
- **SQLite Database Population**: Saves sampled job records to `core_engine/datasets/jobs.db`.
- **PyTorch Tensor Matrix Generation**: Generates pre-computed `(5000, 384)` embedding matrix saved to `core_engine/datasets/dataset_embeddings_cache.pt`.

```bash
uv run python scripts/ingest_qdrant.py
```

### 3. Technical Visualizations: `generate_visuals.py`
Generates high-resolution technical diagrams for reports, presentations, and documentation:
- **System Architecture**: High-level component flowchart.
- **Document Pipeline**: Step-by-step PDF layout sorting, table extraction, and dual-pass OCR pipeline.
- **RAG & Scoring Workflow**: Semantic vector similarity and ATS score calibration workflow.
- **Performance Benchmarks**: VRAM usage and latency benchmarks.

```bash
uv run python scripts/generate_visuals.py
```

### 4. Documentation Converter: `md_to_docs.py`
Converts Markdown documentation files into formatted Microsoft Word (`.docx`) documents using `pandoc`.

```bash
uv run python scripts/md_to_docs.py README.md -o CareerPulse_Report.docx
```
