# Document Extraction & OCR Pipeline Subsystem

The `core_engine/resume_security` module provides high-fidelity PDF document parsing, multi-column layout reconstruction, table extraction, hyperlink harvesting, and adaptive 300 DPI preprocessed OCR fallback for **CareerPulse** with a strict **no-silent-fallbacks** validation policy.

---

## 1. Technical Stack

- **Vector Extraction Engine:** `pdfplumber` (Spatial coordinate sorting, word bounding boxes, table grids, annotation URIs)
- **Line-Wrap Hyphen Repair:** Regex normalization (`re.sub(r'(\w+)-\n(\w+)', r'\1\2')`)
- **OCR Engine:** `pytesseract` (300 DPI dual-pass `--psm 3` Tesseract-OCR)
- **PDF Rasterization:** `pdf2image` & `Poppler` (High-resolution 300 DPI page conversion)
- **Image Preprocessing:** `opencv-python` (CLAHE contrast enhancement, Bilateral edge-preserving filtering, Adaptive Gaussian Thresholding)
- **Error Policy:** Explicit `ValueError` on unreadable/empty PDFs and `RuntimeError` on OCR/dependency failures

---

## 2. Key Capabilities & Progress

- [x] **Multi-Column Spatial Reconstruction**: Extracts words sorted by `(top, x0)` to reconstruct two-column and complex resume layouts without line garbling across columns.
- [x] **Line-Wrap Hyphen Normalization**: Automatically repairs hyphenated split terms (`Py-\nthon` $\to$ `Python`, `Postgre-\nSQL` $\to$ `PostgreSQL`).
- [x] **Structured Table Grid Parsing**: Extracts borderless and bordered tables (education, experience, certifications) into structured text lines.
- [x] **Hyperlink & Annotation Harvesting**: Extracts embedded target URIs (`page.hyperlinks` / `page.annots`) for GitHub, LinkedIn, and personal portfolio links.
- [x] **Page-Level Hybrid OCR Check**: Selectively triggers OCR on individual pages when extracted character density is sparse (< 30 characters).
- [x] **Adaptive 300 DPI Dual-Pass Preprocessed OCR**: Applies OpenCV CLAHE contrast enhancement, bilateral noise filtering, and adaptive Gaussian thresholding, comparing enhanced grayscale vs. binarized passes.
- [x] **Strict Document Validation**: Rejects files yielding $< 20$ characters or failed OCR passes with explicit exceptions.

---

## 3. Directory Structure

```text
core_engine/resume_security/
├── README.md       # Subsystem documentation (this file)
├── __init__.py     # Package marker
├── router.py       # FastAPI router defining /api/v1/security/upload
└── service.py      # SecurityService: spatial extraction, table parsing, links, and dual-pass OCR
```

---

## 4. Extraction Pipeline Details

The extraction pipeline is implemented in `SecurityService.process_resume(file)` in `service.py`:

```
Uploaded PDF
     │
     ▼
[ pdfplumber Vector Extraction ]
     ├─► Hyperlink & Annotation Harvesting (GitHub, LinkedIn, URIs)
     ├─► Borderless & Bordered Table Extraction
     ├─► Multi-Column Spatial Layout Sorting (top, x0)
     └─► Line-Wrap Hyphen Normalization (re.sub)
     │
     ▼
[ Sparsity Check: Character Count < 30 per page? ]
     ├─► NO  ──► Yield Extracted Clean Document Text
     └─► YES ──► Trigger 300 DPI Adaptive Dual-Pass OCR Fallback
                     │
                     ▼
          [ pdf2image Rasterization (300 DPI) ]
                     │
                     ▼
          [ OpenCV Preprocessing Pipeline ]
             • CLAHE Contrast Enhancement
             • Bilateral Noise Filter (Edge Preserving)
             • Adaptive Gaussian Thresholding
                     │
                     ▼
          [ Dual-Pass Tesseract OCR (--psm 3) ]
             • Pass 1: Enhanced Grayscale Frame
             • Pass 2: Binarized Adaptive Frame
                     │
                     ▼
          [ Minimum Length Check: Extracted Text >= 20 chars? ]
             • YES ──► Return High-Fidelity Clean Text
             • NO  ──► Raise Explicit ValueError / RuntimeError
```

---

## 5. Endpoints & Methods

### `router.py`
- `POST /api/v1/security/upload`: Accepts PDF file upload, validates `.pdf` extension, executes `security_service.process_resume(file)`, and returns extracted raw text and security report.

### `service.py` (`SecurityService`)
- `process_resume(file)`: High-level orchestrator returning `text`, `redacted_text`, and `security_report`. Raises `ValueError` if extracted text $< 20$ characters.
- `_extract_raw_text(content)`: Multi-column spatial layout parser with table extraction and hyphen repair.
- `_extract_hyperlinks(page)`: Harvests embedded URLs from PDF annotations.
- `_extract_tables_text(page)`: Formats tabular grids into readable text lines.
- `_ocr_image_dual_pass(image)`: Dual-pass OpenCV preprocessed OCR pipeline using `pytesseract`.

---

## 6. System Prerequisites

1. **Tesseract-OCR**: Required for OCR execution (`winget install UB-Mannheim.TesseractOCR`).
2. **Poppler**: Required by `pdf2image` for PDF rasterization.
