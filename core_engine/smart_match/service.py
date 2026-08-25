import re
from sentence_transformers import util
from core_engine.smart_match.schemas import SmartMatchRequest, SmartMatchResponse, MultiJobMatchResponse, JobMatchResult
from core_engine.embedding_service import embedding_service
from core_engine.data_layer.service import data_layer_service
from core_engine.llm_service import llm_service
from typing import List, Set

STOP_WORDS = {
    "and", "or", "with", "in", "of", "for", "the", "a", "an", "to", "skills", 
    "experience", "development", "programming", "knowledge", "ability", "proficient",
    "understanding", "working", "strong", "excellent", "good", "hands-on"
}

COMMON_TECH_DICT = [
    "python", "java", "c++", "c#", "javascript", "typescript", "php", "ruby", "go", "golang", "rust", "swift", "kotlin",
    "react", "react.js", "angular", "vue", "vue.js", "node", "node.js", "express", "fastapi", "django", "flask", "spring", "bootstrap", "tailwind",
    "docker", "kubernetes", "k8s", "aws", "azure", "gcp", "terraform", "ansible", "jenkins", "ci/cd", "linux", "bash", "shell",
    "sql", "postgresql", "mysql", "mongodb", "redis", "qdrant", "elasticsearch", "oracle", "sqlite",
    "pytorch", "tensorflow", "keras", "scikit-learn", "sklearn", "opencv", "nltk", "spacy", "huggingface", "llm", "rag", "sbert", "bert",
    "pandas", "numpy", "tableau", "powerbi", "excel", "spark", "hadoop", "kafka", "git", "github", "jira", "figma", "rest", "api", "graphql", "grpc",
    "system design", "microservices", "oop", "data structures", "algorithms"
]

def is_skill_in_text(skill_phrase: str, text_lower: str) -> bool:
    """
    Token-aware skill matcher that checks direct substrings, exact token boundaries,
    and technical term lemmas to accurately recognize skills across resumes and JDs.
    """
    phrase_clean = skill_phrase.lower().strip()
    if not phrase_clean:
        return False

    # 1. Direct substring match
    if phrase_clean in text_lower:
        return True

    # 2. Tokenize phrase into core technical terms
    tokens = [t for t in re.findall(r'\b[a-zA-Z0-9\+#\.\-]{2,20}\b', phrase_clean) if t not in STOP_WORDS]
    if not tokens:
        return False

    # 3. Check if any core technical token matches as word boundary in text
    for token in tokens:
        if len(token) >= 2 and re.search(r'\b' + re.escape(token) + r'\b', text_lower):
            return True

    return False

class SmartMatchService:
    async def match_against_database(
        self, 
        resume_text: str, 
        limit: int = 5,
        qualification: str = None,
        strict_qualification: bool = True
    ) -> MultiJobMatchResponse:
        """
        Retrieves top JDs from database and computes detailed match for each.
        """
        top_jobs = data_layer_service.search_jobs(
            resume_text, 
            limit=limit, 
            qualification=qualification, 
            strict_qualification=strict_qualification
        )
        
        results = []
        for job in top_jobs:
            portal_str = f"Job Portal: {job.job_portal}\n" if job.job_portal else ""
            resp_str = f"Responsibilities: {job.responsibilities}\n" if job.responsibilities else ""
            exp_str = f"{job.experience} Years" if job.experience is not None else "Not specified"
            
            full_jd_text = (
                f"Title: {job.title}\n"
                f"Role: {job.role or job.title}\n"
                f"Company: {job.company}\n"
                f"Location: {job.location}, {job.country}\n"
                f"Experience Required: {exp_str}\n"
                f"Qualifications: {job.qualifications}\n"
                f"Salary Range: {job.salary_range}\n"
                f"Work Type: {job.work_type}\n"
                f"{portal_str}"
                f"Required Skills: {', '.join(job.skills)}\n"
                f"{resp_str}"
                f"Description: {job.description}"
            )
            req = SmartMatchRequest(resume_text=resume_text, jd_text=full_jd_text)
            match_details = await self.calculate_match(req, dynamic_skills=job.skills)
            
            results.append(JobMatchResult(
                job_id=job.id,
                job_title=job.title,
                role=job.role or job.title,
                company=job.company,
                location=job.location,
                country=job.country,
                experience=job.experience,
                qualifications=job.qualifications,
                salary_range=job.salary_range,
                work_type=job.work_type,
                skills=job.skills,
                responsibilities=job.responsibilities,
                description=job.description,
                job_portal=job.job_portal,
                preference=job.preference,
                contact_person=job.contact_person,
                contact=job.contact,
                company_profile=job.company_profile,
                match_details=match_details
            ))
            
        return MultiJobMatchResponse(top_matches=results)

    async def calculate_match(self, request: SmartMatchRequest, dynamic_skills: List[str] = None) -> SmartMatchResponse:
        """
        Calculates calibrated semantic ATS match score dynamically based on
        database job requirements, vector similarity, and token-aware skill matching.
        """
        resume_emb = embedding_service.encode(request.resume_text)
        jd_emb = embedding_service.encode(request.jd_text)
        
        cosine_score = util.cos_sim(resume_emb, jd_emb).item()
        
        # SBERT Cosine Calibration (document similarity scale 0.12 -> 0.60 mapped to 0% -> 100%)
        vector_percentage = max(0.0, min(100.0, ((cosine_score - 0.12) / 0.48) * 100))
        
        resume_lower = request.resume_text.lower()
        jd_lower = request.jd_text.lower()
        
        # 1. Collect skills listed in database job
        target_skills: List[str] = []
        if dynamic_skills:
            for s in dynamic_skills:
                clean_s = s.strip()
                if len(clean_s) > 1 and clean_s.lower() not in [ts.lower() for ts in target_skills]:
                    target_skills.append(clean_s)

        # 2. Add common tech dictionary skills present in JD
        for tech in COMMON_TECH_DICT:
            if re.search(r'\b' + re.escape(tech) + r'\b', jd_lower):
                if tech.lower() not in [ts.lower() for ts in target_skills]:
                    target_skills.append(tech.title())

        # 3. Evaluate skill match ratio using token-aware matcher
        matched_skills: List[str] = []
        missing_skills: List[str] = []

        for skill in target_skills:
            if is_skill_in_text(skill, resume_lower):
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

        if target_skills:
            skill_ratio_score = (len(matched_skills) / len(target_skills)) * 100
            # Blend 50% semantic vector alignment + 50% technical skill overlap
            overall_score = round(0.50 * vector_percentage + 0.50 * skill_ratio_score, 1)
        else:
            overall_score = round(vector_percentage, 1)

        # Bound score logically between 10.0% and 98.0%
        overall_score = max(10.0, min(98.0, overall_score))
        
        print(f"DEBUG: Generating LLM feedback (Matched skills: {len(matched_skills)}/{len(target_skills)}) for score {overall_score}%...")
        report = await llm_service.generate_career_advice(
            request.resume_text, request.jd_text, overall_score
        )
        
        # Merge verified matched skills from LLM and token matcher
        combined_matched = list(dict.fromkeys(matched_skills + report.get("matched_skills", [])))
        combined_missing = [s for s in missing_skills if s not in combined_matched]
        
        return SmartMatchResponse(
            overall_score=overall_score,
            justification=report.get("justification", []),
            matched_skills=combined_matched[:15],
            missing_skills=combined_missing[:15],
            recommendations=report.get("recommendations", []),
            career_roadmap=report.get("career_roadmap", [])
        )

smart_match_service = SmartMatchService()
