from sentence_transformers import util
from core_engine.smart_match.schemas import SmartMatchRequest, SmartMatchResponse, MultiJobMatchResponse, JobMatchResult
from core_engine.embedding_service import embedding_service
from core_engine.data_layer.service import data_layer_service
from core_engine.llm_service import llm_service
from typing import List, Tuple

class SmartMatchService:
    async def match_against_database(self, resume_text: str, limit: int = 5) -> MultiJobMatchResponse:
        """
        Retrieves top JDs from the database and calculates detailed match for each.
        """
        # 1. Search for top relevant jobs
        top_jobs = data_layer_service.search_jobs(resume_text, limit=limit)
        
        results = []
        for job in top_jobs:
            # 2. Calculate match for each job
            # Include Title and Skills in the JD text for much better context
            full_jd_text = f"Title: {job.title}\nRequired Skills: {', '.join(job.skills)}\nDescription: {job.description}"
            req = SmartMatchRequest(resume_text=resume_text, jd_text=full_jd_text)
            match_details = await self.calculate_match(req)
            
            results.append(JobMatchResult(
                job_id=job.id,
                job_title=job.title,
                company=job.company,
                match_details=match_details
            ))
            
        return MultiJobMatchResponse(top_matches=results)

    async def calculate_match(self, request: SmartMatchRequest) -> SmartMatchResponse:
        """
        Calculates the semantic match using the shared EmbeddingService
        and generates explainable feedback using the Local LLM.
        """
        # 1. Calculate Score (Embeddings)
        resume_emb = embedding_service.encode(request.resume_text)
        jd_emb = embedding_service.encode(request.jd_text)
        
        cosine_score = util.cos_sim(resume_emb, jd_emb).item()
        overall_score = round(max(0, cosine_score) * 100, 2)
        
        # 2. Generate Explainable Advice (Local LLM)
        # This replaces the old heuristic logic
        print(f"DEBUG: Generating LLM feedback for score {overall_score}%...")
        report = await llm_service.generate_career_advice(
            request.resume_text, request.jd_text, overall_score
        )
        
        return SmartMatchResponse(
            overall_score=overall_score,
            justification=report.get("justification", []),
            matched_skills=report.get("matched_skills", []),
            missing_skills=report.get("missing_skills", []),
            recommendations=report.get("recommendations", []),
            career_roadmap=report.get("career_roadmap", [])
        )

# Singleton instance
smart_match_service = SmartMatchService()
