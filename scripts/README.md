# CareerPulse Utility Scripts (`scripts/`)

This directory contains essential orchestration and automation scripts for the CareerPulse ecosystem. These tools handle data acquisition, vector database initialization, and documentation management.

---

## 1. `setup_data.py` (Data Acquisition)

This script automates the retrieval of job description datasets from Kaggle to ground the RAG (Retrieval-Augmented Generation) pipeline in real-world market data.

### **Functionality**

- Interfaces with the Kaggle API to download specific datasets.
- Automatically unzips files into the `core_engine/data_layer/raw/` directory.
- Ensures required directory structures exist before downloading.

### **Prerequisites**

- Requires a valid `KAGGLE_API_TOKEN` in your `.env` file.

### **Usage**

```powershell
uv run python scripts/setup_data.py
```

---

## 2. `ingest_qdrant.py` (Vector Database Ingestion)

The core data processing script that populates the Qdrant vector database with high-dimensional embeddings.

### **Functionality**

- **CSV Parsing:** Reads raw job descriptions from the data layer.
- **Semantic Vectorization:** Uses the `EmbeddingService` (`all-MiniLM-L6-v2`) to convert text into 384-dimensional vectors.
- **GPU Acceleration:** Automatically leverages CUDA if available for near-instant embedding generation.
- **Metadata Management:** Maps raw CSV columns (Title, Skills, Responsibilities) into structured Qdrant payloads for context-aware retrieval.
- **Batch Processing:** Uploads data in chunks to optimize network throughput and memory usage.

### **Usage**

```powershell
uv run python scripts/ingest_qdrant.py
```

---

## 3. `md_to_docx.py` (Documentation Converter)

A general-purpose document utility designed to bridge the gap between developer-friendly Markdown and academic/professional Word requirements.

### **Functionality**

- **Single File Mode:** Converts a specific `.md` file to a `.docx` file.
- **Batch Mode:** Scans an entire directory and converts all Markdown files found.
- **Professional Formatting:** Utilizes Pandoc's standalone mode to ensure headers and math equations are preserved.
- **Clean Output:** Specifically configured to exclude the Table of Contents (TOC) for a cleaner report layout.

### **Prerequisites**

- Requires **Pandoc** installed on your system (`winget install JohnMacFarlane.Pandoc`).

### **Usage**

**Convert a single file:**

```powershell
uv run python scripts/md_to_docx.py project_assets/Capstone_Report_CareerPulse.md
```

**Convert an entire folder:**

```powershell
uv run python scripts/md_to_docx.py project_assets/
```

**Convert with a custom output name:**

```powershell
uv run python scripts/md_to_docx.py input.md -o Final_Report.docx
```

---

## 4. `generate_visuals.py` (Visual Asset Generator)

A specialized tool for creating professional, publication-quality diagrams and graphs for technical reports and academic submissions.

### **Functionality**

- **Aesthetic Consistency:** Uses a unified "System Design" color palette and typography across all visuals.
- **Hardware Analysis:** Generates VRAM and Latency comparison graphs based on local hardware benchmarks (e.g., RTX 3060).
- **Architecture Visualization:** Produces clean, vector-style diagrams for System Architecture, Security Pipelines, and RAG Workflows.
- **Conceptual Diagrams:** Visualizes complex AI concepts like the "Semantic Gap", "Cosine Similarity", and "PII Redaction".
- **Automated Export:** Saves all visuals directly to `project_assets/images/` for easy inclusion in Markdown or Word documents.

### **Usage**

```powershell
uv run python scripts/generate_visuals.py
```

---

## Technical Notes

- **Environment:** All scripts should be executed via `uv run` to ensure they utilize the project's specific virtual environment and CUDA-optimized dependencies.
- **Logging:** All scripts include `DEBUG` and `SUCCESS` logging to provide real-time status updates in the terminal.
