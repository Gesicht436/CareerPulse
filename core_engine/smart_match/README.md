# Smart Match Engine (`core_engine/smart_match/`)

Implements the core logic for matching job seekers to their ideal roles using state-of-the-art NLP techniques.

---

## 1. Technical Stack

- **Embeddings:**
- **Explainable AI:**
- **Search:**

---

## 2. RAG & Explainable AI

The engine has evolved into a full **RAG (Retrieval-Augmented Generation)** system:

1. **Contextual Retrieval:** Finds top-N relevant JDs from Qdrant based on the resume.
2. **Semantic Scoring:** Uses Sentence-Transformers for alignment calculation.
3. **AI Justification:** A local LLM analyzes the specific skills and experience to provide natural language feedback.

---

## 3. API Usage

### **Search All Jobs:**

Matches a resume against the entire Qdrant database.

### **Compare One-to-One:**

Detailed match report for a specific Job Description.

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
