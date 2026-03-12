# Smart Match Engine (`core_engine/smart_match/`)

Implements the core logic for matching job seekers to their ideal roles using state-of-the-art NLP techniques.

---

## 1. Technical Stack

- **Embeddings:** `sentence-transformers` (Model: `all-MiniLM-L6-v2`).
- **Mathematics:** Cosine Similarity for semantic alignment calculation.
- **Search:** RAG (Retrieval-Augmented Generation) pipeline.
- **LLM:** Local models (planned) for explainable analysis.

---

## 2. Current Implementation: Semantic Matching

The engine has moved beyond keyword matching to **Semantic Matching**. It calculates the "meaning distance" between a Resume and a Job Description.

### **How it works:**

1. **Vectorization:** The entire resume and JD are converted into 384-dimensional dense vectors.
2. **Cosine Similarity:** The engine calculates the angle between these vectors to determine alignment.
3. **Scoring:** The raw similarity is scaled to a 0-100% "Match Score."

---

## 3. API Usage

### **Endpoint:** `POST /api/v1/smart-match/match`

**Request Body:**
```json
{
  "resume_text": "Experienced Python developer with FastAPI expertise...",
  "jd_text": "Looking for a Python developer with FastAPI and Docker experience..."
}
```

**Response Body:**
```json
{
  "overall_score": 89.8,
  "justification": ["Semantic similarity score of 89.8% indicates a strong alignment..."],
  "matched_skills": ["Python", "FastAPI"],
  "missing_skills": ["Kubernetes", "AWS"],
  "recommendations": ["Enhance your profile by adding hands-on experience..."]
}
```

---

## 4. Key Feature Requirements

1. **Context-Aware Retrieval:** Ensuring the RAG system pulls relevant job requirements based on the specific industry context of the resume.
2. **Justification Engine:** Providing clear reasons for the "Readiness Score."
3. **Actionable Roadmap:** Automatically suggesting top 3 learning paths.
4. **Model Benchmarking:** Comparing different embedding models for accuracy.
