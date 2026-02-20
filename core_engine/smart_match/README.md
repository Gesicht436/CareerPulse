# Smart Match Engine (`core_engine/smart_match/`)

Implements the core logic for matching job seekers to their ideal roles using state-of-the-art NLP techniques.

---

## 1. Technical Stack

- **Search:** RAG (Retrieval-Augmented Generation).
- **Embeddings:** Sentence-Transformers or Local LLM embeddings.
- **LLM:** Local models (Qwen3 8B, GPTOSS) for explainable analysis.

---

## 2. Key Responsibilities

### **Mayank Anand**
- **Semantic Matching:** Moving beyond keyword density to true semantic similarity.
- **Explainable AI:** Generating detailed reports on *why* a resume matches or fails to match a JD.
- **Skill Gap Analysis:** Identifying missing competencies based on the `data_pipeline` taxonomy.
- **Optimization:** Tuning the RAG pipeline for both accuracy and inference speed.

---

## 3. Key Feature Requirements

1. **Context-Aware Retrieval:** Ensuring the RAG system pulls relevant job requirements based on the specific industry context of the resume.
2. **Justification Engine:** Providing the user with clear, bulleted reasons for their "Readiness Score" (e.g., "Matched on Cloud Architecture, missed on Kubernetes").
3. **Actionable Roadmap:** Automatically suggesting top 3 learning paths or certifications based on the identified skill gaps.
4. **A/B Testing Framework:** Ability to compare different embedding models to measure which provides better matching accuracy.
