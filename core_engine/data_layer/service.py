import os
from typing import List, Optional, Any
import torch
from core_engine.data_layer.schemas import JobDescriptionModel
from core_engine.data_layer.database import fetch_jobs_by_ids, DB_PATH
from core_engine.embedding_service import embedding_service

EMBEDDINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "embeddings")
EMBEDDINGS_FULL_PATH = os.path.join(EMBEDDINGS_DIR, "dataset_embeddings_full.pt") if os.path.exists(os.path.join(EMBEDDINGS_DIR, "dataset_embeddings_full.pt")) else os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "dataset_embeddings_full.pt")
META_FULL_PATH = os.path.join(EMBEDDINGS_DIR, "dataset_meta_full.pt") if os.path.exists(os.path.join(EMBEDDINGS_DIR, "dataset_meta_full.pt")) else os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "dataset_meta_full.pt")

DEGREE_GROUPS = {
    "engineering": ["b.tech", "m.tech", "bca", "mca", "b.e", "computer science", "engineering"],
    "business": ["mba", "bba", "b.com", "m.com", "business", "finance", "marketing", "management"],
    "arts": ["ba", "bachelor of arts", "arts", "humanities"],
    "research": ["phd", "ph.d", "doctorate", "research"]
}

DEGREE_CODE_MAP = {
    "engineering": 1,
    "business": 2,
    "arts": 3,
    "research": 4
}

class DataLayerService:
    """
    High-Performance Zero-Docker Data Layer for CareerPulse.
    Operates strictly across the full 1,615,940 jobs dataset using:
    - In-memory PyTorch FP16 Vector Tensor Matrix (dataset_embeddings_full.pt)
    - Zero-Object GPU/CPU Matrix Multiplication (torch.matmul)
    - High-Speed Indexed SQLite Batch Retrieval (jobs.db)
    """
    def __init__(self):
        self._full_embeddings_matrix: Optional[torch.Tensor] = None
        self._full_job_ids: Optional[List[str]] = None
        self._full_degree_codes: Optional[torch.Tensor] = None

    def _ensure_dataset_loaded(self):
        """
        Validates dataset existence and loads the 1.61M FP16 PyTorch vector matrix into memory.
        Raises FileNotFoundError if dataset artifacts are missing (Strict Error Policy).
        """
        if not os.path.exists(EMBEDDINGS_FULL_PATH):
            raise FileNotFoundError(
                f"Full vector matrix not found at '{EMBEDDINGS_FULL_PATH}'. "
                "Please run 'uv run python scripts/ingest_full_dataset.py' to generate the 1.61M vector database."
            )
        if not os.path.exists(META_FULL_PATH):
            raise FileNotFoundError(
                f"Dataset metadata not found at '{META_FULL_PATH}'. "
                "Please run 'uv run python scripts/ingest_full_dataset.py' to generate dataset metadata."
            )
        if not os.path.exists(DB_PATH):
            raise FileNotFoundError(
                f"SQLite jobs database not found at '{DB_PATH}'. "
                "Please run 'uv run python scripts/ingest_full_dataset.py' to initialize the database."
            )

        if self._full_embeddings_matrix is None:
            print(f"DEBUG: Loading 1.61M FP16 PyTorch vector matrix from '{EMBEDDINGS_FULL_PATH}'...")
            self._full_embeddings_matrix = torch.load(EMBEDDINGS_FULL_PATH, weights_only=False).to(torch.float32)
            meta = torch.load(META_FULL_PATH, weights_only=False)
            self._full_job_ids = meta["job_ids"]
            self._full_degree_codes = meta["degree_codes"]
            print(f"DEBUG: Loaded {len(self._full_job_ids):,} vector embeddings into memory successfully.")

    def search_jobs(
        self, 
        query_text: str, 
        limit: int = 5, 
        experience_level: str = None,
        qualification: str = None,
        strict_qualification: bool = True
    ) -> List[JobDescriptionModel]:
        """
        Scans the entire 1.61M vector space using Section-Aware Weighted Vector Embedding Ranking.
        Executes parallel PyTorch matrix operations and retrieves the top winning records from SQLite.
        """
        self._ensure_dataset_loaded()

        headline_query = query_text[:400]
        query_embs = embedding_service.encode([headline_query, query_text], batch_size=2, convert_to_tensor=True)
        query_headline_emb = query_embs[0].to(torch.float32)
        query_full_emb = query_embs[1].to(torch.float32)

        matrix = self._full_embeddings_matrix
        job_ids = self._full_job_ids
        degree_codes = self._full_degree_codes

        target_indices = None
        if strict_qualification and qualification:
            qual_lower = qualification.lower().strip()
            target_code = 0
            for group_name, keywords in DEGREE_GROUPS.items():
                if any(k in qual_lower for k in keywords):
                    target_code = DEGREE_CODE_MAP.get(group_name, 0)
                    break
            
            if target_code > 0:
                mask = (degree_codes == target_code)
                target_indices = torch.nonzero(mask, as_tuple=True)[0]
                if len(target_indices) == 0:
                    raise ValueError(f"No job descriptions matching qualification '{qualification}' were found in the database.")
                matrix = matrix[target_indices]
                print(f"DEBUG: Degree Filter ACTIVE ('{qualification}'): Scanning {len(target_indices):,} matching jobs.")

        # Align tensor devices and dtypes for fast matrix multiplication
        v_head = query_headline_emb.to(device=matrix.device, dtype=matrix.dtype)
        v_full = query_full_emb.to(device=matrix.device, dtype=matrix.dtype)

        # Section-Aware Matrix Multiplication: 40% Headline + 60% Full Body
        sim_headline = torch.matmul(matrix, v_head)
        sim_full = torch.matmul(matrix, v_full)
        blended_sims = (0.40 * sim_headline) + (0.60 * sim_full)

        top_k_indices = torch.topk(blended_sims, k=min(limit, len(blended_sims))).indices.tolist()

        if target_indices is not None:
            winning_job_ids = [job_ids[target_indices[i].item()] for i in top_k_indices]
        else:
            winning_job_ids = [job_ids[i] for i in top_k_indices]

        # High-speed indexed batch retrieval from SQLite
        results = fetch_jobs_by_ids(winning_job_ids)
        if not results:
            raise RuntimeError(f"Failed to fetch matched job records from SQLite for IDs: {winning_job_ids[:5]}")
        return results

data_layer_service = DataLayerService()
