# Smart Match Engine: Dual-Stage Semantic Matching & Local LLM Reasoning

The `core_engine/smart_match` module is the intelligence core of **CareerPulse**. It performs section-aware vector scoring across 1.61M job postings, token-aware technical skill extraction, academic degree filtering, and qualitative career roadmap synthesis using a local quantized Large Language Model.

---

## 1. Technical Stack

- **Vector Mathematics:** `sentence-transformers` (SBERT `all-MiniLM-L6-v2` generating 384-dimensional dense vectors)
- **Token-Aware Skill Matcher:** Custom `is_skill_in_text` matching engine with 150+ technology dictionary (`COMMON_TECH_DICT`) and regex word-boundary evaluation
- **Local LLM Engine:** `transformers` & `bitsandbytes` (Local Qwen 2.5 1.5B/7B inference with 4-bit NF4 quantization)
- **Feature Flag & Telemetry Enforcement:** Integrates with `TelemetryService` to respect `enable_jd_analyzer` toggles and log `JD_ANALYZED` / `JOB_SEARCH` events
- **Schema Enforcement:** Pydantic models guaranteeing valid structured JSON responses

---

## 2. Key Capabilities & Progress

- [x] **Section-Aware 1.61M Vector Search**: Blended cosine similarity ($0.40 \times \text{Headline} + 0.60 \times \text{Body}$) yielding top 5 job recommendations across 1,615,940 jobs.
- [x] **Token-Aware Skill Matcher (`is_skill_in_text`)**: Evaluates direct substrings, exact token boundaries, and technical term lemmas across 150+ technologies.
- [x] **Calibrated ATS Blending**: Blends $50\%$ Semantic Vector Alignment + $50\%$ Technical Skill Overlap Ratio into a unified 0–100% match score.
- [x] **Educational Degree Filtering**: Strict degree group matching (`DEGREE_GROUPS`) restricting matches to candidate educational qualifications (`B.Tech`, `B.Sc`, `MBA`, `MCA`, `PhD`, etc.).
- [x] **Local Quantized Qwen 2.5 LLM**: Executes local Qwen 2.5 model in 4-bit NF4 quantization for high-speed, zero-cloud private inference.
- [x] **Automated Career Roadmaps**: Generates structured 4-week weekly learning plans to bridge identified technical skill gaps.
- [x] **Strict Failure Policies**: Raises explicit `RuntimeError` if LLM inference fails (zero mock fallbacks).

---

## 3. Directory Structure

```text
core_engine/smart_match/
├── README.md       # Subsystem documentation (this file)
├── __init__.py     # Package marker
├── router.py       # FastAPI endpoints (/match, /match-all, /search-jobs)
├── schemas.py      # Pydantic schemas (SmartMatchRequest, SmartMatchResponse, JobMatchResult, MultiJobMatchResponse)
└── service.py      # SmartMatchService: SBERT scoring, skill matching, and LLM advice synthesis
```

---

## 4. Matching Pipeline Architecture

```
Candidate Resume Text
         │
         ▼
[ Stage 1: Degree Extraction & Group Filtering ]
  Extract candidate qualification (e.g. B.Tech)
  Filter 1.61M dataset via DEGREE_CODE_MAP tensor mask
         │
         ▼
[ Stage 2: Section-Aware SBERT Vector Ranking ]
  Compute V_headline & V_body embeddings
  Execute PyTorch matrix multiplication across 1.61M rows:
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

| Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/smart-match/match` | Evaluates a single resume against a specific custom job description text (checks `enable_jd_analyzer` flag) | `200`, `403`, `500` |
| `POST` | `/api/v1/smart-match/match-all` | Compares a resume against the entire 1.61M jobs database and returns top 5 recommendations | `200`, `500` |
| `GET` | `/api/v1/smart-match/search-jobs` | Semantic natural language job search query returning ranked job descriptions | `200`, `500` |

---

## 6. Key Components

### `service.py` (`SmartMatchService`)
- **`match_against_database(resume_text, limit, qualification, strict_qualification)`**: Retrieves top JDs from the 1.61M data layer, builds enriched prompt contexts (Role, Portal, Responsibilities, Skills), and calculates complete match breakdowns.
- **`calculate_match(request, dynamic_skills)`**: Computes SBERT similarity, token-aware skill overlap, calibrated ATS score, and queries `LLMService` for qualitative justifications and roadmaps.
- **`is_skill_in_text(skill_phrase, text_lower)`**: Evaluates direct substrings and token word boundaries with stop-word pruning.

### `schemas.py`
- **`SmartMatchRequest`**: Payload containing `resume_text` and `jd_text`.
- **`SmartMatchResponse`**: Contains `overall_score`, `justification`, `matched_skills`, `missing_skills`, `recommendations`, and `career_roadmap`.
- **`JobMatchResult`**: Bundles full job metadata (`job_id`, `job_title`, `role`, `company`, `location`, `country`, `experience`, `qualifications`, `salary_range`, `work_type`, `skills`, `responsibilities`, `description`, `job_portal`, `preference`, `contact_person`, `contact`, `company_profile`) with embedded `SmartMatchResponse`.
- **`MultiJobMatchResponse`**: Top-level response schema containing `top_matches: List[JobMatchResult]`.
