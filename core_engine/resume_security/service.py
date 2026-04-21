import pdfplumber
import re
import spacy
from typing import List, Dict, Any, Tuple
from fastapi import UploadFile

class SecurityService:
    def __init__(self):
        # Load spaCy model for PII detection
        try:
            # We use the full name of the package we installed
            self.nlp = spacy.load("en_core_web_sm")
            print("DEBUG: spaCy model 'en_core_web_sm' loaded successfully.")
        except Exception as e:
            print(f"DEBUG: Failed to load spaCy model: {e}")
            self.nlp = None

    async def process_resume(self, file: UploadFile) -> Dict[str, Any]:
        """
        Main pipeline for processing an uploaded resume PDF.
        Returns extracted text and security audit results.
        """
        content = await file.read()
        print(f"DEBUG: Processing file: {file.filename}, Size: {len(content)} bytes")
        
        # 1. Extraction and Hidden Text Detection
        text, security_flags = self._extract_text_and_check_hidden(content)
        print(f"DEBUG: Extracted text length: {len(text)} characters")
        if len(text.strip()) < 50:
            print("DEBUG WARNING: Very little text extracted. PDF might be an image or have complex encoding.")
        
        # 2. PII Validation
        pii_entities = self._detect_pii(text)
        redacted_text = text
        if pii_entities:
            print(f"DEBUG: PII Entities detected: {len(pii_entities)}")
            redacted_text = self._redact_pii(text, pii_entities)
            security_flags.append({
                "type": "PII_DETECTED",
                "detail": f"PII detected and redacted: {', '.join(list(set([e[1] for e in pii_entities]))[:3])}",
                "severity": "medium" # Lowered from high because we are redacting it now
            })

        # 3. Prompt Injection Check
        injection_found = self._check_prompt_injection(text)
        if injection_found:
            print("DEBUG: Prompt injection patterns matched.")
            security_flags.append({
                "type": "PROMPT_INJECTION",
                "detail": "Potential prompt injection attempt detected.",
                "severity": "critical"
            })

        return {
            "text": text,
            "redacted_text": redacted_text,
            "security_report": {
                "is_safe": not any(f["severity"] in ["high", "critical"] for f in security_flags),
                "flags": security_flags
            }
        }

    def _redact_pii(self, text: str, entities: List[Tuple[str, str]]) -> str:
        """
        Replaces detected PII entities with their labels to protect privacy.
        """
        # Sort entities by length descending to avoid partial replacements
        sorted_entities = sorted(entities, key=lambda x: len(x[0]), reverse=True)
        redacted = text
        for ent_text, ent_label in sorted_entities:
            # Simple replacement for now. In a production system, we'd use 
            # more sophisticated masking to avoid breaking context.
            redacted = redacted.replace(ent_text, f"[{ent_label}]")
        return redacted

    def _extract_text_and_check_hidden(self, content: bytes) -> Tuple[str, List[Dict]]:
        flags = []
        all_text = []
        
        import io
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                print(f"DEBUG: pdfplumber opened PDF. Total pages: {len(pdf.pages)}")
                for i, page in enumerate(pdf.pages):
                    # Strategy: Try layout-preserved extraction first
                    page_text = page.extract_text(layout=True) or page.extract_text() or ""
                    all_text.append(page_text)
                    
                    # Check for hidden text (white-on-white)
                    chars = page.chars
                    if not chars and not page_text.strip():
                        print(f"DEBUG: Page {i+1} has no characters or text layer.")
                    
                    for char in chars:
                        # Improved color check
                        color = char.get('non_stroking_color')
                        # White in RGB is usually (1, 1, 1) or (255, 255, 255)
                        is_white = False
                        if isinstance(color, (list, tuple)):
                            if all(c > 0.95 for c in color) or all(c > 250 for c in color):
                                is_white = True
                        
                        if is_white or char.get('size', 10) < 1:
                            flags.append({
                                "type": "HIDDEN_TEXT",
                                "detail": f"Hidden text detected on page {i+1}",
                                "severity": "medium"
                            })
                            break
            
            combined_text = "\n".join(all_text)
            # If text is too short, it might be a scanned PDF. Trigger OCR.
            if len(combined_text.strip()) < 100:
                print("DEBUG: Text layer too thin. Triggering OCR fallback...")
                ocr_text = self._extract_text_via_ocr(content)
                if len(ocr_text.strip()) > len(combined_text.strip()):
                    combined_text = ocr_text
                    flags.append({
                        "type": "OCR_APPLIED",
                        "detail": "Resume was processed using OCR as it appeared to be a scanned image.",
                        "severity": "info"
                    })

        except Exception as e:
            print(f"DEBUG ERROR: pdfplumber failed: {e}")
            # Fallback to OCR if pdfplumber fails entirely
            combined_text = self._extract_text_via_ocr(content)
            if not combined_text:
                return "", [{"type": "PARSE_ERROR", "detail": str(e), "severity": "high"}]
        
        return combined_text, flags

    def _extract_text_via_ocr(self, content: bytes) -> str:
        from pdf2image import convert_from_bytes
        import pytesseract
        import numpy as np
        import cv2

        print("DEBUG: Attempting OCR extraction...")
        try:
            # Note: poppler must be installed and in PATH for pdf2image to work
            images = convert_from_bytes(content)
            ocr_text = []
            for i, image in enumerate(images):
                # Convert PIL image to OpenCV format
                open_cv_image = np.array(image)
                # Convert RGB to BGR 
                open_cv_image = open_cv_image[:, :, ::-1].copy()
                gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
                # Apply thresholding to improve OCR accuracy
                thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                
                text = pytesseract.image_to_string(thresh)
                ocr_text.append(text)
                print(f"DEBUG: OCR processed page {i+1}")
            return "\n".join(ocr_text)
        except Exception as e:
            print(f"DEBUG ERROR: OCR failed: {e}. Ensure Tesseract and Poppler are installed.")
            return ""

    def _detect_pii(self, text: str) -> List[Tuple[str, str]]:
        if not self.nlp:
            return []
        
        # Tech whitelist: words that should NEVER be redacted even if spaCy thinks they are PERSON/ORG
        TECH_WHITELIST = {
            "azure", "docker", "aws", "kubernetes", "python", "java", "javascript", 
            "react", "angular", "node", "typescript", "git", "github", "gitlab",
            "sql", "mysql", "postgresql", "mongodb", "redis", "linux", "unix",
            "windows", "macos", "ios", "android", "flutter", "dart", "kotlin",
            "swift", "c#", "c++", "ruby", "rails", "php", "laravel", "django",
            "flask", "fastapi", "spring", "dotnet", "asp.net", "entity framework"
        }

        doc = self.nlp(text[:10000]) # Limit to first 10k chars for perf
        
        # Removed ORG and GPE as they are too prone to redacting tech skills or useful locations
        pii_labels = ["PERSON", "EMAIL", "PHONE"] 
        
        entities = []
        for ent in doc.ents:
            if ent.label_ in pii_labels:
                # Check whitelist
                if ent.text.lower().strip() in TECH_WHITELIST:
                    continue
                entities.append((ent.text, ent.label_))
        
        # Simple regex fallbacks for Email/Phone if spaCy misses
        email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        phone_regex = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
        
        emails = re.findall(email_regex, text)
        phones = re.findall(phone_regex, text)
        
        for email in emails:
            entities.append((email, "EMAIL"))
        for phone in phones:
            entities.append((phone, "PHONE"))
            
        return list(set(entities))

    def _check_prompt_injection(self, text: str) -> bool:
        patterns = [
            r"ignore (all )?previous instructions",
            r"system (prompt|message)",
            r"new instructions",
            r"forget what I said",
            r"act as a",
            r"you must (always )?give"
        ]
        text_lower = text.lower()
        return any(re.search(p, text_lower) for p in patterns)

security_service = SecurityService()
