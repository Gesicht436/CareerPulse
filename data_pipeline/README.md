# Data Pipeline (`data_pipeline/`)

The engine for data ingestion, ensuring the system has a constant stream of fresh Job Descriptions and a robust skill taxonomy.

---

## 1. Technical Stack

- **Scraping:** Scrapy
- **Processing:** Pandas, spaCy, NLTK
- **Orchestration:** Prefect
- **Storage:** PostgreSQL + Qdrant

---

## 2. Work Distribution

### **Ankit (Lead) & Mayank**

- **Web Scraping:** Building and maintaining spiders for job boards (Indeed, Kaggle datasets).
- **Data Preprocessing:**
  - Text cleaning and deduplication.
  - Formatting data for spaCy entity recognition.
- **Skill Taxonomy:**
  - Maintaining the "Skill Dictionary" used for gap analysis.
  - Categorizing skills into "Must-have" vs. "Nice-to-have" based on market trends.
- **Pipeline Orchestration:** Using Prefect to schedule and monitor data ingestion tasks.

---

## 3. Key Feature Requirements

1. **Automated Deduplication:** Logic to prevent the same job posting from being ingested multiple times from different sources.
2. **Schema-Agnostic Ingestion:** A flexible parser that can handle varying JD formats from diverse platforms.
3. **Dynamic Taxonomy Updates:** A mechanism to flag and review new "trending skills" (e.g., "RAG Engineering") that appear in fresh JDs.
4. **Pipeline Health Monitoring:** Visual dashboard (via Prefect) showing success/failure rates of daily scraping jobs.
