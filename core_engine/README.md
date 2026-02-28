# Core Engine (`core_engine/`)

The **Core Engine** is the central nervous system of CareerPulse. It handles the orchestration of security checks, semantic matching, and data persistence via a high-performance API.

---

## 1. Technical Stack

- **Framework:** FastAPI
- **Server:** Uvicorn + Gunicorn
- **Validation:** Pydantic v2
- **Auth:** OAuth2 + JWT (Passlib)
- **Security:** SlowAPI (Rate Limiting)
- **NLP:** spaCy, pdfplumber, regex + unicode normalization

---

## 2. Work Distribution

### **Mayank Anand (Team Lead)**

- **API Gateway:** Designing the modular RESTful API structure under `/api/v1`.
- **System Orchestration:** Managing the flow between `resume_security`, `smart_match`, and `data_layer`.
- **Infrastructure:** Containerization and deployment logic using Docker.

---

## 3. Sub-Modules

- **[`data_layer/`](./data_layer/):** Manages PostgreSQL (user data) and Qdrant (vector embeddings).
- **[`resume_security/`](./resume_security/):** Handles adversarial AI defense and PII redaction.
- **[`smart_match/`](./smart_match/):** Executes RAG-based matching between resumes and JDs.

---

## 4. Key Feature Requirements

1. **Modular Routing:** Clean separation of concerns between security, matching, and data endpoints.
2. **Robust Middleware:** Global error handling and security headers for all API responses.
3. **Stateless Auth:** Secure JWT-based authentication with appropriate token expiration and refresh logic.
4. **Rate Limiting:** IP-based and user-based throttling to prevent API abuse.

---

## 5. Development Setup

```bash
cd core_engine
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
