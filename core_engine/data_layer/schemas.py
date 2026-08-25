from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union

class CompanyProfileModel(BaseModel):
    sector: Optional[str] = Field(None, description="Business sector")
    industry: Optional[str] = Field(None, description="Specific industry")
    city: Optional[str] = Field(None, description="Headquarters city")
    state: Optional[str] = Field(None, description="Headquarters state")
    zip: Optional[str] = Field(None, description="Postal code")
    website: Optional[str] = Field(None, description="Company website URL")
    ticker: Optional[str] = Field(None, description="Stock ticker symbol")
    ceo: Optional[str] = Field(None, description="Chief Executive Officer")

class JobDescriptionModel(BaseModel):
    id: str = Field(..., description="Unique identifier for the job")
    title: str = Field(..., description="General job title")
    role: Optional[str] = Field(None, description="Specific job function / role specialization")
    company: str = Field(..., description="Company name")
    location: Optional[str] = Field(None, description="City / municipal job location")
    country: Optional[str] = Field(None, description="Country")
    work_type: Optional[str] = Field(None, description="Employment type (e.g. Full-Time, Intern, Contract)")
    experience: Optional[Union[int, str]] = Field(None, description="Required experience in normalized years")
    qualifications: Optional[str] = Field(None, description="Required qualifications (e.g. B.Tech, MBA, BCA, PhD)")
    salary_range: Optional[str] = Field(None, description="Compensation range (e.g. $56K-$116K)")
    skills: List[str] = Field(default_factory=list, description="Extracted technical and domain skills")
    responsibilities: Optional[str] = Field(None, description="Key role duties and responsibilities")
    description: str = Field(..., description="Full job description text")
    job_portal: Optional[str] = Field(None, description="Portal where the job is posted (e.g. Snagajob, Idealist, LinkedIn)")
    preference: Optional[str] = Field(None, description="Posting preference if any (e.g. Both, Female, Male)")
    contact_person: Optional[str] = Field(None, description="Recruiter contact person")
    contact: Optional[str] = Field(None, description="Recruiter contact info")
    company_profile: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Enriched company profile metadata (Sector, Industry, Website, CEO)")
