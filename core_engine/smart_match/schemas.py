from pydantic import BaseModel, Field
from typing import List, Optional

class SmartMatchRequest(BaseModel):
    resume_text: str = Field(..., description="The full text content of the resume.")
    jd_text: str = Field(..., description="The full text content of the job description.")
    user_id: Optional[str] = None

class SkillMatch(BaseModel):
    skill_name: str
    is_matched: bool
    relevance_score: float

class SmartMatchResponse(BaseModel):
    overall_score: float = Field(..., ge=0, le=100, description="The semantic matching score between 0 and 100.")
    justification: List[str] = Field(..., description="Bullet points explaining why the resume matches or fails to match the JD.")
    matched_skills: List[str] = Field(..., description="Skills from the JD that were found in the resume.")
    missing_skills: List[str] = Field(..., description="Key skills from the JD that are missing in the resume.")
    recommendations: List[str] = Field(..., description="Top 3 actionable steps to improve the matching score.")
