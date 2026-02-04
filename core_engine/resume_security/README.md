# Resume Security Module

## Overview

A specialized library for handling raw resume files, ensuring privacy, and detecting security threats.

## Responsibilities

- **Parsing:** Extract text from PDF/DOCX.
- **PII Redaction:** Identify and mask sensitive info (Email, Phone, Address).
- **Adversarial Defense:** Detect hidden text, prompt injection, and other "Resume Smuggler" attacks.

## Key Functions

- `parse_resume(file)`
- `redact_pii(text)`
- `detect_adversarial(text, metadata)`

## Dependencies

- spaCy
- PyPDF2 / pdfminer.six
