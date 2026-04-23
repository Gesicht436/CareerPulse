from pydantic import BaseModel, Field
from typing import Optional, List

class JobDescriptionModel(BaseModel):
    id: str = Field(..., description="Unique identifier for the job")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: Optional[str] = Field(None, description="Job location")
    country: Optional[str] = Field(None, description="Country")
    description: str = Field(..., description="Full job description text")
    skills: List[str] = Field(default_factory=list, description="Extracted skills for the job")
    experience: Optional[str] = Field(None, description="Required experience")
    qualifications: Optional[str] = Field(None, description="Required qualifications")
    salary_range: Optional[str] = Field(None, description="Salary range")
    work_type: Optional[str] = Field(None, description="Employment type (e.g. Full-time, Part-time)")
