# Smart Match Engine: Dual-Stage Semantic Analysis

## Technical Stack

- **Similarity Engine:** `sentence-transformers` (SBERT for high-speed vector math)
- **Token-Aware Skill Matcher:** `is_skill_in_text` (Token boundary matching with 150+ tech dictionary)
- **Local LLM:** `transformers` (Hugging Face implementation of Qwen 2.5)
- **Quantization:** `bitsandbytes` (4-bit NF4 quantization for low VRAM usage)
- **Inference Optimization:** `accelerate` (Dynamic device mapping for CUDA/CPU)
- **Schema Enforcement:** `pydantic` (Ensuring structured LLM JSON responses)
- **Data Serialization:** Python `json`, `re` (Robust parsing of LLM outputs)

---

## Key Progress

- [x] **Semantic Scoring & Calibration:** SBERT Cosine Similarity scaled over $[0.12, 0.60] \to [0\%, 100\%]$.
- [x] **Token-Aware Technical Skill Matcher:** `is_skill_in_text` token boundary matching evaluating technical skill overlap ratios accurately.
- [x] **Multi-Factor ATS Blending:** $50\%$ Semantic Vector Alignment + $50\%$ Technical Skill Overlap Ratio.
- [x] **Educational Degree Filtering:** Degree group matching (`DEGREE_GROUPS`) restricting matches to candidate educational qualifications (`B.Tech`, `B.Sc`, `MBA`, etc.).
- [x] **LLM Integration:** Wired Local LLM for qualitative reasoning and feedback.
- [x] **Structured Analysis:** Enforced strict JSON schema for LLM outputs.
- [x] **Skill Gap Logic:** Automated extraction of missing vs. matched skills.
- [x] **Roadmap Generation:** Context-aware 4-week learning path development.

---

The **Smart Match Engine** is the intelligence hub of CareerPulse. It moves beyond simple keyword counting to perform deep, contextual analysis of professional alignment. By combining high-speed vector mathematics, token-aware skill matching, and the nuanced reasoning of Large Language Models (LLMs), the engine provides candidates with more than just a score—it provides a personalized roadmap to career success.

## The Multi-Stage Matching Architecture

### Stage 1: Section-Aware Vector Search & Degree Filtering
- **Vector Retrieval**: Computes SBERT embeddings with section-aware hybrid weighting ($0.40 \times \text{Headline} + 0.60 \times \text{Body}$).
- **Degree Qualification Filter**: Applies degree group matching (`DEGREE_GROUPS`) when `strict_qualification=True`, restricting dataset postings to jobs matching candidate degree qualifications (`B.Tech`, `B.Sc`, `MBA`, etc.).

### Stage 2: Token-Aware Skill Matcher & Score Calibration
- **Token Matcher (`is_skill_in_text`)**: Tokenizes skill phrases and matches core technical terms against candidate resume text using a built-in 150+ tech dictionary.
- **Calibrated Blended ATS Score**: $\text{ATS Score} = 0.50 \times \text{Vector Similarity \%} + 0.50 \times \text{Skill Overlap \%}$.

### Stage 3: Qualitative LLM Reasoning (Local Qwen 2.5)
- Triggers the **LLM Service** (Qwen 2.5 1.5B/7B) to perform qualitative evaluation.
- Enforces strict JSON output containing:
  - **Justification**: Key reasons why the score was assigned.
  - **Skill Gap Analysis**: Verified matched vs missing technical skills.
  - **Actionable Recommendations**: Concrete steps to improve alignment.
  - **Career Roadmap**: Multi-week learning plan to master missing skills.

---

## Module Components

### `router.py` (API Layer)
Exposes matching capabilities via FastAPI (`/match`, `/search-jobs`).

### `schemas.py` (Data Structures)
Pydantic models (`SmartMatchResponse`, `JobMatchResult`, `MultiJobMatchResponse`).

### `service.py` (Orchestrator)
 coordinates vector search, token-aware skill matching, degree filtering, and LLM advice.
