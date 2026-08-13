# Document Processing & OCR Extraction Subsystem

## Technical Stack

- **Vector Extraction Engine:** `pdfplumber` (Spatial multi-column layout reconstruction, table grid extraction, hyperlink harvesting)
- **Hyphen Normalization Engine:** `re` (Line-wrap hyphen joining `Py-\nthon` $\to$ `Python`)
- **OCR Engine:** `pytesseract` (300 DPI dual-pass `--psm 3` Tesseract-OCR)
- **PDF Processing:** `pdf2image`, `Poppler` (300 DPI page rasterization for OCR fallback)
- **Image Preprocessing:** `opencv-python` (CLAHE contrast enhancement, Bilateral noise filtering, Adaptive Gaussian thresholding)

---

## Key Progress

- [x] **Multi-Column Spatial Reconstruction**: Words sorted by `(top, x0)` to preserve two-column resume layouts without garbling text across columns.
- [x] **Line-Wrap Hyphen Normalization**: Automatically joins hyphenated words across line breaks (`Py-\nthon` $\to$ `Python`, `Postgre-\nSQL` $\to$ `PostgreSQL`).
- [x] **Structured Table Extraction**: Parses borderless and bordered grid tables into clean text lines.
- [x] **Hyperlink & Annotation Harvesting**: Extracts embedded target URIs (`page.hyperlinks` / `page.annots`) for GitHub, LinkedIn, and personal portfolio links.
- [x] **Page-Level Hybrid OCR**: Selectively triggers OCR per page when character density is sparse (< 30 characters).
- [x] **300 DPI Dual-Pass Preprocessed OCR**: Applies OpenCV CLAHE contrast enhancement, bilateral filtering, and adaptive Gaussian thresholding, comparing enhanced grayscale and thresholded passes.

---

## The Extraction Pipeline

The core of this module is the `process_resume` method in `service.py`, which orchestrates high-fidelity document text conversion.

### 1. Vector PDF Extraction (`pdfplumber`)

- **Spatial Multi-Column Reconstruction**: Uses word coordinate sorting (`round(top/3)*3, x0`) in `pdfplumber` to reconstruct multi-column layouts without merging text horizontally across columns.
- **Table Extraction**: Parses structured matrix grids (education, experience, certification blocks) into text lines (`Col1 | Col2`).
- **Hyperlink Harvesting**: Extracts embedded target URIs (`uri` attributes) for LinkedIn profiles, GitHub repos, and personal portfolios to enrich candidate alignment vectors.
- **Hyphen Normalization**: Applies regex normalization (`re.sub(r'(\w+)-\n(\w+)', r'\1\2')`) to repair broken technical terms.

### 2. Adaptive Preprocessed OCR Fallback (300 DPI)

For scanned or image-only PDFs, the engine executes an advanced OpenCV-preprocessed OCR fallback:

- **300 DPI Rasterization**: `pdf2image.convert_from_bytes(content, dpi=300)` renders high-resolution page images.
- **CLAHE Contrast Enhancement**: Applies Contrast Limited Adaptive Histogram Equalization (`cv2.createCLAHE`) to boost text contrast on colored or gradient headers.
- **Bilateral Noise Filtering**: Removes image noise while preserving font edges (`cv2.bilateralFilter`).
- **Adaptive Gaussian Thresholding**: Binarizes unevenly lit or shaded backgrounds (`cv2.adaptiveThreshold`).
- **Dual-Pass Tesseract OCR**: Runs Tesseract (`--psm 3`) on enhanced grayscale and binarized frames, selecting the pass yielding maximum high-quality text output.

---

## File Details

### `router.py`
The FastAPI router handles PDF file uploads via `/api/v1/security/upload`, validating file format before delegating text extraction to `SecurityService`.

### `service.py`
Implements `SecurityService` as a singleton. Handles:

- **Vector Extraction & Normalization**: `_extract_raw_text()` and `_extract_page_text_optimized()`.
- **Table & Link Extraction**: `_extract_tables_text()` and `_extract_hyperlinks()`.
- **Preprocessed OCR**: `_ocr_image_dual_pass()`, `_extract_single_page_ocr()`, and `_extract_text_via_ocr()`.

---

## Requirements & Setup

1. **Tesseract-OCR**: Required for OCR fallback.
2. **Poppler**: Required by `pdf2image` for 300 DPI PDF page rasterization.
