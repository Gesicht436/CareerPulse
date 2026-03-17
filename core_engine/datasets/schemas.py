from pydantic import BaseModel, Field
from typing import Optional, List

class JobDescriptionModel(BaseModel):
    id: str = Field(..., description="Unique identifier for the job")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: Optional[str] = Field(None, description="Job location")
    description: str = Field(..., description="Full job description text")
    skills: List[str] = Field(default_factory=list, description="Extracted skills for the job")
