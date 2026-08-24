# CareerPulse Quality Assurance: Test Suite & Hardware Diagnostics

The `quality_assurance/` directory contains the automated test suite, integration verifications, and hardware diagnostic tools for **CareerPulse**. It ensures the reliability of core API endpoints, authentication flows, semantic matching pipelines, and CUDA GPU acceleration.

---

## 1. Test Directory Overview

| File | Purpose | Coverage Area | Key Dependencies |
| :--- | :--- | :--- | :--- |
| `cuda_check.py` | PyTorch & CUDA hardware diagnostic script | GPU detection, VRAM access, Torchvision NMS | `torch`, `torchvision` |
| `test_api.py` | FastAPI endpoint & JSON serialization test | Basic gateway health & route handling | `pytest`, `fastapi.testclient` |
| `test_auth.py` | Full authentication flow integration test | Sign-Up (`/signup`), Sign-In (`/login`), Session (`/me`) | `pytest`, `fastapi.testclient`, `core_engine` |
| `test_main.py` | Gateway application availability test | Gateway root endpoint (`/`) & response status | `pytest`, `fastapi.testclient` |
| `test_smart_match.py` | Semantic matching pipeline test | Core engine imports & matching service verification | `pytest`, `fastapi.testclient`, `core_engine` |

---

## 2. Subsystem Testing Breakdown

### A. Authentication Pipeline (`test_auth.py`)
Verifies user onboarding, password hashing, and token validation:
1. **User Sign-Up (`POST /api/v1/auth/signup`)**: Tests user registration, PBKDF2 salt generation (100,000 rounds), and JWT token issuance.
2. **User Sign-In (`POST /api/v1/auth/login`)**: Validates credential authentication and token retrieval.
3. **Session Verification (`GET /api/v1/auth/me`)**: Validates Bearer token authorization headers, role claims (`user` / `admin`), and user profile retrieval.

### B. Core Gateway & API Health (`test_api.py` & `test_main.py`)
- Verifies FastAPI route resolution, CORS middleware application, and status 200 JSON responses.
- Ensures fast response times without requiring heavy AI model loading during basic health checks.

### C. Smart Matcher Subsystem (`test_smart_match.py`)
- Tests core engine module initialization and validates SBERT embedding and local LLM services.

### D. Hardware & CUDA Acceleration Diagnostic (`cuda_check.py`)
Checks system GPU readiness for local LLM inference (Qwen 2.5 4-bit) and SentenceTransformer embedding generation:
- Displays PyTorch version (`torch.__version__`) and CUDA availability (`torch.cuda.is_available()`).
- Identifies active NVIDIA GPU device name and device index.
- Validates `torchvision.ops.nms` availability for computer vision / OCR sub-tasks.

---

## 3. How to Run Tests

### Run Full Test Suite
```bash
uv run python -m pytest quality_assurance/
```

### Run a Specific Test Module
```bash
uv run python -m pytest quality_assurance/test_auth.py
```

### Run CUDA Hardware Diagnostics
```bash
uv run python quality_assurance/cuda_check.py
```

---

## 4. Test Expectations & Standards

- **Passing Criterion**: 100% of test cases in `quality_assurance/` must pass cleanly without unhandled exceptions or failed assertions.
- **Embedded & Zero-Docker Architecture**: Tests execute against the embedded SQLite database (`jobs.db`) and local user store (`users_db.json`), requiring no external Docker containers.
