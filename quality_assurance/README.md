# Quality Assurance (`quality_assurance/`)

Ensuring the reliability, security, and performance of CareerPulse through rigorous automated testing.

---

## 1. Technical Stack

- **Testing:** `pytest`, `pytest-asyncio`
- **Security:** `Atheris` (Fuzzing)
- **Property-based Testing:** `Hypothesis`
- **Performance:** `Locust`
- **API Clients:** `httpx` (for async integration testing)

---

## 2. Running Tests

To run the full suite or specific modules, ensure you are in the project root and have your environment synced with `uv`.

### **Smart Match Engine Tests**

Verifies the semantic matching logic with similar and dissimilar profiles.
```bash
$env:PYTHONPATH="."
uv run pytest quality_assurance/test_smart_match.py -s
```

---

## 3. Work Distribution

### **Abhinav 08 (Lead)**

- **Security Benchmarking:**
  - Crafting adversarial resumes to test the `resume_security` module.
- **Performance Testing:** Benchmarking latency for embedding generation and matching.
- **Coverage & Compliance:**
  - Enforcing >80% unit test coverage.
- **Load Testing:** Simulating high-traffic scenarios using Locust.

---

## 4. Key Feature Requirements

1. **Adversarial Test Suite:** A collection of "poisoned" resumes specifically designed to break the parsing logic.
2. **Automated Performance Regression:** Failing CI/CD if API response times increase.
3. **Property-Based API Tests:** Using Hypothesis to ensure the API never returns a 500 error.
4. **Fuzzing Reports:** Reports discovery of edge cases during fuzzing.
