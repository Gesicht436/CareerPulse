# Smart Match Engine: Dual-Stage Semantic Analysis

## Technical Stack

- **Similarity Engine:** `sentence-transformers` (SBERT for high-speed vector math)
- **Local LLM:** `transformers` (Hugging Face implementation of Qwen 2.5)
- **Quantization:** `bitsandbytes` (4-bit NF4 quantization for low VRAM usage)
- **Inference Optimization:** `accelerate` (Dynamic device mapping for CUDA/CPU)
- **Schema Enforcement:** `pydantic` (Ensuring structured LLM JSON responses)
- **Data Serialization:** Python `json`, `re` (Robust parsing of LLM outputs)

---

## Key Progress

- [x] **Semantic Scoring:** Implemented SBERT-based Cosine Similarity for raw alignment.
- [x] **LLM Integration:** Wired Local LLM for qualitative reasoning and feedback.
- [x] **Structured Analysis:** Enforced strict JSON schema for LLM outputs.
- [x] **Skill Gap Logic:** Automated extraction of missing vs. matched skills.
- [x] **Roadmap Generation:** Context-aware 4-week learning path development.
- [x] **Context Augmentation:** Pre-processing of JDs with titles and key metadata.
- [x] **Fallback Mechanisms:** Robust error handling for LLM "hallucinations".
- [ ] **Multi-Candidate Ranking:** Logic to rank multiple resumes against one JD.
- [ ] **Weight Tuning:** Custom scoring weights for experience vs. education.
- [ ] **Streaming Inference:** Support for server-sent events (SSE) for LLM progress.

The **Smart Match Engine** is the intelligence hub of CareerPulse. It moves beyond simple keyword counting to perform deep, contextual analysis of professional alignment. By combining high-speed vector mathematics with the nuanced reasoning of Large Language Models (LLMs), the engine provides candidates with more than just a "score"—it provides a personalized roadmap to career success.

## The Two-Stage Matching Architecture

The core philosophy of the engine is that machines should do the math and AI should do the reasoning. This is implemented in the `SmartMatchService` through two distinct stages.

### Stage 1: Mathematical Contextual Alignment (Embeddings)

Before any qualitative analysis happens, the engine calculates a **Semantic Similarity Score**.

- **Vector Transformation**: The resume text (redacted for privacy) and the job description are transformed into 384-dimensional vectors using the `EmbeddingService`. This process captures the semantic essence of the text. For example, the engine learns that "proficient in Python" and "experienced in back-end development with Django" are mathematically similar.
- **Cosine Similarity Calculation**: We use the formula for Cosine Similarity: `(A · B) / (||A|| ||B||)`. This calculates the cosine of the angle between the two vectors. A score closer to 1 (or 100%) indicates nearly identical professional alignment.
- **Normalization and Thresholding**: The raw similarity score is rounded and bounded between 0 and 100. This provides a fast, initial ranking that allows the system to filter out completely irrelevant jobs before performing more expensive AI analysis.

### Stage 2: Qualitative Reasoning (Local LLM)

Once a baseline score is established, the engine triggers the **LLM Service** (Qwen 2.5 1.5B/7B) to perform a human-like evaluation.

- **Expert Analysis**: The LLM acts as a "Senior Technical Recruiter." It receives the resume, the JD, and the calculated score as context.
- **Structured JSON Generation**: Unlike traditional LLM outputs, our engine enforces a strict JSON schema. This allows the backend to programmatically extract:
  - **Justification**: A list of three key reasons why the score was assigned.
  - **Skill Gap Analysis**: A precise comparison of technical skills present vs. missing.
  - **Actionable Recommendations**: Five concrete steps the user can take to improve their specific resume for this specific job.
- **Career Roadmap**: The engine generates a structured, multi-week learning plan designed to help the candidate master the "missing skills" identified during the matching process.

## Module Components

### `router.py` (API Layer)

This file exposes the matching capabilities to the world through FastAPI.

- **`/match`**: Analyzes a single resume against a specific, provided job description. This is ideal for a "check my resume against this job link" feature.
- **`/match-all`**: This is the more powerful endpoint. It takes a resume and performs a **Reverse Search** across the entire Qdrant database. It finds the top 5 jobs and performs the Stage 2 LLM analysis for *each* of them, returning a comprehensive career report.

### `schemas.py` (Data Structures)

We use complex Pydantic models to ensure the frontend receives rich, typed data.

- **`SmartMatchResponse`**: Contains the score, justifications, skill lists, and the roadmap.
- **`MultiJobMatchResponse`**: A collection of `JobMatchResult` objects, allowing the dashboard to display a list of relevant jobs, each with its own full AI report.

### `service.py` (Orchestrator)

The `SmartMatchService` class is a singleton that coordinates all other services.

- **Context Augmentation**: Before sending data to the LLM, the service prepends the job title and core skills to the JD text. This "Context Pre-Injection" significantly improves the LLM's ability to focus on the most important requirements.
- **Error Handling and Fallbacks**: If the LLM fails (due to memory issues or invalid output), the service catches the exception and returns a "System Detected" fallback report, ensuring the user experience never breaks.

## Performance & Scalability

- **Batch Processing**: When using `/match-all`, the Stage 1 vector search is extremely fast, while Stage 2 LLM analysis is executed sequentially to manage VRAM usage.
- **Asynchronous Execution**: The entire module is built using `async/await` patterns, allowing the FastAPI server to handle multiple matching requests concurrently without blocking the main event loop.
- **GPU Optimization**: If a GPU is present, the engine utilizes it for both vector math (Stage 1) and transformer inference (Stage 2), reducing matching time from 30+ seconds to under 5 seconds.
