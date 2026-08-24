# Smart Match Engine: Dual-Stage Semantic Matching & Local LLM Reasoning

The `core_engine/smart_match` module is the intelligence core of **CareerPulse**. It performs section-aware vector scoring, token-aware technical skill extraction, academic degree filtering, and qualitative career roadmap synthesis using a local quantized Large Language Model.

---

## 1. Technical Stack

- **Vector Mathematics:** `sentence-transformers` (SBERT `all-MiniLM-L6-v2` generating 384-dimensional dense vectors)
- **Token-Aware Skill Matcher:** Custom `is_skill_in_text` matching engine with 150+ technology dictionary and regex word-boundary evaluation
- **Local LLM Engine:** `transformers` & `bitsandbytes` (Local Qwen 2.5 1.5B/7B inference with 4-bit NF4 quantization)
- **Inference Optimization:** Dynamic CUDA GPU allocation with CPU fallback support
- **Schema Enforcement:** Pydantic models guaranteeing valid structured JSON responses

---

## 2. Key Capabilities & Progress

- [x] **Section-Aware Vector Search**: Blended cosine similarity ($0.40 \times \text{Headline} + 0.60 \times \text{Body}$) yielding top 5 job recommendations.
- [x] **Token-Aware Skill Matcher (`is_skill_in_text`)**: Evaluates direct substrings, exact token boundaries, and technical term lemmas across 150+ technologies.
- [x] **Calibrated ATS Blending**: Blends $50\%$ Semantic Vector Alignment + $50\%$ Technical Skill Overlap Ratio into a unified 0–100% match score.
- [x] **Educational Degree Filtering**: Strict degree group matching (`DEGREE_GROUPS`) restricting matches to candidate educational qualifications (`B.Tech`, `B.Sc`, `MBA`, etc.).
- [x] **Local Quantized Qwen 2.5 LLM**: Executes local Qwen 2.5 model in 4-bit NF4 quantization for high-speed, zero-cloud private inference.
- [x] **Automated Career Roadmaps**: Generates structured 4-week weekly learning plans to bridge identified technical skill gaps.

---

## 3. Directory Structure

```text
core_engine/smart_match/
├── README.md       # Subsystem documentation (this file)
├── __init__.py     # Package marker
├── router.py       # FastAPI endpoints (/match, /match-all, /search-jobs)
├── schemas.py      # Pydantic schemas (SmartMatchRequest, SmartMatchResponse, JobMatchResult)
└── service.py      # SmartMatchService: SBERT scoring, skill matching, and LLM advice
```

---

## 4. Matching Pipeline Architecture

```
Candidate Resume Text
         │
         ▼
[ Stage 1: Degree Extraction & Group Filtering ]
  Extract candidate qualification (e.g. B.Tech)
  Filter SQLite dataset via DEGREE_GROUPS
         │
         ▼
[ Stage 2: Section-Aware SBERT Vector Ranking ]
  Compute V_headline & V_body embeddings
  Execute PyTorch cosine similarity matrix multiplication:
  Score = 0.40 * Sim(Headline) + 0.60 * Sim(Body)
  Select Top 5 Candidates
         │
         ▼
[ Stage 3: Token-Aware Technical Skill Overlap ]
  Evaluate 150+ technology dictionary against text
  Compute Matched Skills & Missing Skill Gaps
  Calibrate ATS Score: 50% Vector + 50% Skill Overlap
         │
         ▼
[ Stage 4: Local Qwen 2.5 LLM Qualitative Reasoning ]
  Synthesize Match Justifications
  Identify Detailed Actionable Recommendations
  Construct Tailored Weekly Career Learning Roadmap
```

---

## 5. API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/smart-match/match` | Evaluates a single resume against a specific custom job description text |
| `POST` | `/api/v1/smart-match/match-all` | Compares a resume against the entire SQLite database and returns top 5 recommendations |
| `GET` | `/api/v1/smart-match/search-jobs` | Semantic job search query returning ranked job descriptions |

---

## 6. Key Components

### `service.py` (`SmartMatchService`)
- **`match_against_database(resume_text, limit, qualification, strict_qualification)`**: Retrieves top JDs from the data layer and calculates complete match breakdowns.
- **`calculate_match(request, dynamic_skills)`**: Computes SBERT similarity, token-aware skill overlap, calibrated ATS score, and queries `LLMService` for qualitative justifications and roadmaps.

### `schemas.py`
- **`SmartMatchRequest`**: Payload containing `resume_text` and `jd_text`.
- **`SmartMatchResponse`**: Contains `semantic_score`, `skill_score`, `overall_score`, `matched_skills`, `missing_skills`, `justification`, `recommendations`, and `career_roadmap`.
- **`JobMatchResult`**: Bundles job metadata with embedded `SmartMatchResponse`.
