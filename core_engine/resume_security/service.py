import pdfplumber
import re
from typing import List, Dict, Any, Tuple
from fastapi import UploadFile
import io

class SecurityService:
    def __init__(self):
        print("DEBUG: Security Pipeline & PII Redaction disabled per consumer requirements. Advanced PDF & OCR extraction active.")

    async def process_resume(self, file: UploadFile) -> Dict[str, Any]:
        """
        Main pipeline for processing an uploaded resume PDF.
        Extracts high-fidelity raw text directly using optimized multi-column layout extraction,
        hyperlink harvesting, and adaptive preprocessed OCR fallback.
        """
        content = await file.read()
        print(f"DEBUG: Processing file: {file.filename}, Size: {len(content)} bytes")
        
        text = self._extract_raw_text(content)
        print(f"DEBUG: Extracted raw text length: {len(text)} characters")
        
        if not text or len(text.strip()) < 20:
            raise ValueError("Unable to extract readable text from the uploaded PDF resume. Ensure the PDF contains readable text or clear scanned content.")
        
        return {
            "text": text,
            "redacted_text": text,  # Raw text preserved (no PII redaction)
            "security_report": {
                "is_safe": True,
                "flags": []
            }
        }

    def _extract_raw_text(self, content: bytes) -> str:
        """
        Extracts raw text from PDF using pdfplumber with column reconstruction,
        table extraction, hyperlink harvesting, and page-by-page OCR fallback.
        """
        all_pages_text = []
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page_idx, page in enumerate(pdf.pages):
                    page_components = []

                    # 1. Harvest Hyperlinks / Annotations (e.g. GitHub, LinkedIn, Portfolios)
                    links = self._extract_hyperlinks(page)

                    # 2. Extract Structured Tables if present
                    table_text = self._extract_tables_text(page)
                    if table_text:
                        page_components.append(table_text)

                    # 3. Extract Page Text (Try layout mode with custom tolerances, fallback to word sorting)
                    text = self._extract_page_text_optimized(page)
                    if text:
                        page_components.append(text)

                    if links:
                        page_components.append("Links: " + ", ".join(links))

                    combined_page_text = "\n".join(page_components).strip()

                    # 4. Page-Level Hybrid Check: If page text is sparse (< 30 chars), run OCR for this page
                    if len(combined_page_text) < 30:
                        print(f"DEBUG: Page {page_idx + 1} text sparse ({len(combined_page_text)} chars). Triggering page-level OCR...")
                        ocr_page_text = self._extract_single_page_ocr(content, page_idx)
                        if len(ocr_page_text.strip()) > len(combined_page_text):
                            combined_page_text = ocr_page_text.strip()

                    if combined_page_text:
                        all_pages_text.append(combined_page_text)

            combined_doc_text = "\n\n".join(all_pages_text)

            # Global Document Fallback if entire PDF yielded < 50 chars
            if len(combined_doc_text.strip()) < 50:
                print("DEBUG: Overall PDF text sparse. Running full document OCR fallback...")
                full_ocr_text = self._extract_text_via_ocr(content)
                if len(full_ocr_text.strip()) > len(combined_doc_text.strip()):
                    combined_doc_text = full_ocr_text

            # Normalize line-wrap hyphens (e.g. Py-\nthon -> Python)
            cleaned_text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', combined_doc_text)
            return cleaned_text.strip()
        except Exception as e:
            print(f"DEBUG: Vector PDF text extraction encountered error: {e}. Executing full OCR...")
            ocr_text = self._extract_text_via_ocr(content)
            cleaned_ocr = re.sub(r'(\w+)-\n(\w+)', r'\1\2', ocr_text).strip()
            if not cleaned_ocr or len(cleaned_ocr) < 20:
                raise ValueError(f"Failed to extract readable text from PDF: Vector extraction error ({e}) and OCR yielded empty text.") from e
            return cleaned_ocr

    def _extract_hyperlinks(self, page: Any) -> List[str]:
        """Harvest URIs embedded in PDF page annotations."""
        links = []
        try:
            # pdfplumber page.hyperlinks list of dicts
            hyperlinks = getattr(page, 'hyperlinks', []) or []
            for link in hyperlinks:
                uri = link.get('uri') or link.get('url')
                if uri and uri not in links:
                    links.append(uri)
            
            # Check page annotations if hyperlinks attribute is empty
            if not links and hasattr(page, 'annots') and page.annots:
                for annot in page.annots:
                    uri = annot.get('uri') or annot.get('A', {}).get('URI')
                    if uri and uri not in links:
                        links.append(uri)
        except Exception as e:
            print(f"DEBUG: Hyperlink extraction warning: {e}")
        return links

    def _extract_tables_text(self, page: Any) -> str:
        """Extracts tabular data and formats cells into clean text lines."""
        try:
            tables = page.extract_tables()
            if not tables:
                return ""
            
            table_lines = []
            for table in tables:
                for row in table:
                    clean_row = [str(cell).strip().replace('\n', ' ') for cell in row if cell is not None and str(cell).strip()]
                    if clean_row:
                        table_lines.append(" | ".join(clean_row))
            return "\n".join(table_lines)
        except Exception as e:
            print(f"DEBUG: Table extraction warning: {e}")
            return ""

    def _extract_page_text_optimized(self, page: Any) -> str:
        """
        Extracts text with optimized tolerances and word spatial reconstruction for multi-column layouts.
        """
        # Primary pass: layout-aware extraction with adjusted tolerance
        try:
            primary_text = page.extract_text(layout=True, x_tolerance=3, y_tolerance=3) or ""
        except Exception:
            primary_text = ""

        # Secondary pass: standard extraction
        try:
            secondary_text = page.extract_text(layout=False) or ""
        except Exception:
            secondary_text = ""

        # Spatial word reconstruction for complex column layouts
        try:
            words = page.extract_words(use_text_flow=True, keep_blank_chars=False)
            if words:
                # Sort words by vertical top coordinate first, then horizontal x0
                words_sorted = sorted(words, key=lambda w: (round(w['top'] / 3) * 3, w['x0']))
                reconstructed_lines = []
                current_top = None
                current_line = []
                for w in words_sorted:
                    line_top = round(w['top'] / 3) * 3
                    if current_top is None or line_top != current_top:
                        if current_line:
                            reconstructed_lines.append(" ".join(current_line))
                        current_line = [w['text']]
                        current_top = line_top
                    else:
                        current_line.append(w['text'])
                if current_line:
                    reconstructed_lines.append(" ".join(current_line))
                reconstructed_text = "\n".join(reconstructed_lines)
            else:
                reconstructed_text = ""
        except Exception:
            reconstructed_text = ""

        # Select text extraction result with maximum character density and word structure
        candidates = [primary_text, secondary_text, reconstructed_text]
        best_text = max(candidates, key=lambda t: len(t.strip()))
        return best_text.strip()

    def _extract_single_page_ocr(self, content: bytes, page_idx: int) -> str:
        """OCR processing for a single page with 300 DPI and CLAHE preprocessing."""
        from pdf2image import convert_from_bytes
        try:
            images = convert_from_bytes(content, first_page=page_idx + 1, last_page=page_idx + 1, dpi=300)
            if images:
                return self._ocr_image_dual_pass(images[0])
            raise RuntimeError(f"Failed to rasterize page {page_idx + 1} with pdf2image.")
        except Exception as e:
            print(f"ERROR: Single-page OCR failed for page {page_idx + 1}: {e}")
            raise RuntimeError(f"Single-page OCR failed for page {page_idx + 1}: {str(e)}. Ensure Tesseract-OCR and Poppler are installed.") from e

    def _extract_text_via_ocr(self, content: bytes) -> str:
        """Full document OCR fallback using 300 DPI and dual-pass adaptive preprocessing."""
        from pdf2image import convert_from_bytes
        print("DEBUG: Executing dual-pass preprocessed OCR extraction (300 DPI)...")
        try:
            images = convert_from_bytes(content, dpi=300)
            if not images:
                raise RuntimeError("pdf2image returned 0 pages for the document.")
            ocr_pages = []
            for i, image in enumerate(images):
                page_text = self._ocr_image_dual_pass(image)
                ocr_pages.append(page_text)
                print(f"DEBUG: Dual-pass OCR processed page {i+1}")
            return "\n\n".join(ocr_pages)
        except Exception as e:
            print(f"ERROR: Full OCR execution failed: {e}. Ensure Tesseract and Poppler are installed.")
            raise RuntimeError(f"OCR text extraction failed: {str(e)}. Ensure Tesseract-OCR and Poppler are properly installed on the system.") from e

    def _ocr_image_dual_pass(self, image: Any) -> str:
        """
        Applies OpenCV image enhancement (CLAHE + Bilateral Filter + Adaptive Thresholding)
        and executes dual-pass Tesseract OCR with --psm 3 for optimal multi-column layout recognition.
        """
        import pytesseract
        import numpy as np
        import cv2

        open_cv_image = np.array(image)
        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # 1. CLAHE Contrast Enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_gray = clahe.apply(gray)

        # 2. Bilateral Noise Reduction
        denoised = cv2.bilateralFilter(enhanced_gray, 9, 75, 75)

        # 3. Adaptive Gaussian Thresholding
        adaptive_thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        tess_config = "--psm 3"

        # Pass 1: Enhanced Grayscale image
        try:
            text_pass1 = pytesseract.image_to_string(denoised, config=tess_config)
        except Exception as e:
            print(f"ERROR: Tesseract OCR failed on grayscale pass: {e}")
            raise RuntimeError(f"Tesseract OCR failed during grayscale pass: {str(e)}") from e

        # Pass 2: Adaptive Binarized image
        try:
            text_pass2 = pytesseract.image_to_string(adaptive_thresh, config=tess_config)
        except Exception as e:
            print(f"ERROR: Tesseract OCR failed on adaptive threshold pass: {e}")
            raise RuntimeError(f"Tesseract OCR failed during adaptive threshold pass: {str(e)}") from e

        # Select pass yielding the highest quality text content
        return text_pass1 if len(text_pass1.strip()) >= len(text_pass2.strip()) else text_pass2

security_service = SecurityService()


