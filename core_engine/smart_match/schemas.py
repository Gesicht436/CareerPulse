from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class SmartMatchRequest(BaseModel):
    resume_text: str = Field(..., description="The full text of the resume")
    jd_text: str = Field(..., description="The full text of the job description")

class SmartMatchResponse(BaseModel):
    overall_score: float = Field(..., description="Semantic match score (0-100)")
    justification: List[str] = Field(default_factory=list, description="Reasons for the match score")
    matched_skills: List[str] = Field(default_factory=list, description="Skills found in both resume and JD")
    missing_skills: List[str] = Field(default_factory=list, description="Skills present in JD but missing in resume")
    recommendations: List[str] = Field(default_factory=list, description="Advice to improve the match")
    career_roadmap: List[Dict[str, Any]] = Field(default_factory=list, description="Step-by-step learning path")

class JobMatchResult(BaseModel):
    job_id: str
    job_title: str
    company: str
    match_details: SmartMatchResponse

class MultiJobMatchResponse(BaseModel):
    top_matches: List[JobMatchResult]
