# Quality Assurance (`quality_assurance/`)

Ensuring the reliability, security, and performance of CareerPulse through rigorous automated testing.

---

## 1. Technical Stack

- **Testing:** Pytest, pytest-cov
- **Security:** Atheris (Fuzzing)
- **Property-based Testing:** Hypothesis
- **API Testing:** Postman + Newman
- **Performance:** Locust

---

## 2. Work Distribution

### **Abhinav 08 (Lead)**

- **Security Benchmarking:**
  - Crafting adversarial resumes to test the `resume_security` module.
  - Performing fuzz testing on file upload endpoints using Atheris.
- **Performance Testing:** Benchmarking latency for embedding generation and matching.
- **Coverage & Compliance:**
  - Enforcing >80% unit test coverage.
  - Setting up automated regression suites for every PR.
- **Load Testing:** Simulating high-traffic scenarios using Locust.

---

## 3. Key Feature Requirements

1. **Adversarial Test Suite:** A collection of "poisoned" resumes specifically designed to break the parsing and security logic.
2. **Automated Performance Regression:** Failing CI/CD pipelines if API response times for semantic matching increase beyond a defined threshold.
3. **Property-Based API Tests:** Using Hypothesis to send randomized but valid inputs to ensure the API never returns a 500 error.
4. **Fuzzing Reports:** Weekly reports on edge cases discovered by Atheris during automated fuzzing sessions.
