from typing import List, Dict, Any
from core_engine.data_layer.database import qdrant, QDRANT_COLLECTION
from core_engine.data_layer.schemas import JobDescriptionModel
from core_engine.embedding_service import embedding_service

class DataLayerService:
    def search_jobs(self, query_text: str, limit: int = 5, experience_level: str = None) -> List[JobDescriptionModel]:
        """
        Takes a query text (like a resume or a job title), generates an embedding,
        and retrieves the most semantically relevant job descriptions from Qdrant.
        Supports filtering by experience level.
        """
        # Use shared embedding service
        query_vector = embedding_service.encode(query_text).tolist()
        
        # Prepare filter if provided
        query_filter = None
        if experience_level:
            from qdrant_client.http import models as rest
            query_filter = rest.Filter(
                must=[
                    rest.FieldCondition(
                        key="experience_level",
                        match=rest.MatchValue(value=experience_level)
                    )
                ]
            )

        # Search Qdrant
        query_response = qdrant.query_points(
            collection_name=QDRANT_COLLECTION,
            query=query_vector,
            limit=limit,
            query_filter=query_filter,
            with_payload=True
        )
        
        # Map results to our Pydantic Schema
        # QueryResponse has a 'points' attribute which is a list of ScoredPoint
        jobs = []
        for result in query_response.points:
            payload = result.payload or {}
            job = JobDescriptionModel(
                id=str(result.id),
                title=payload.get("title", "Unknown Title"),
                company="External Platform", # The dataset doesn't seem to have a company column
                location=None,
                description=payload.get("description", ""),
                skills=payload.get("skills", [])
            )
            jobs.append(job)
            
        return jobs

# Singleton instance
data_layer_service = DataLayerService()
