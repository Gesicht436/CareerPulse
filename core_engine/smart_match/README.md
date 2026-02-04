# Smart Match Module

## Overview

The AI engine responsible for semantic analysis, embeddings, and RAG (Retrieval Augmented Generation).

## Responsibilities

- **Embeddings:** Generate vector representations of Resumes and JDs.
- **RAG:** Retrieve relevant skills/jobs from the vector database.
- **Scoring:** Calculate "Career Readiness Score" (Cosine Similarity).
- **Explanation:** Provide feedback on missing skills.

## Key Functions

- `generate_embedding(text)`
- `calculate_similarity(resume_vec, job_vec)`
- `analyze_skill_gap(resume_text, job_description)`

## Dependencies

- Sentence Transformers
- ChromaDB / FAISS
- LangChain (Optional, for orchestration)
