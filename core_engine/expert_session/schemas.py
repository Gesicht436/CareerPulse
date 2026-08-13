from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ExpertProfile(BaseModel):
    id: str = Field(..., description="Unique ID for the expert")
    name: str = Field(..., description="Full name of the industry expert")
    title: str = Field(..., description="Job title / Designation (e.g. Principal Architect at Google)")
    company: str = Field(..., description="Company name")
    domain: str = Field(..., description="Domain expertise (e.g. AI/ML, Cloud Architecture, Frontend)")
    bio: str = Field(..., description="Short professional bio")
    rating: float = Field(default=5.0, description="Average rating out of 5")
    total_sessions: int = Field(default=0, description="Total completed sessions")
    avatar_url: Optional[str] = Field(None, description="Avatar image URL")

class BookingRequest(BaseModel):
    expert_id: str = Field(..., description="Target expert ID")
    applicant_name: str = Field(..., description="Applicant's name")
    applicant_email: str = Field(..., description="Applicant's contact email")
    scheduled_time: str = Field(..., description="Scheduled ISO time string")
    notes: Optional[str] = Field(None, description="Initial notes or specific questions for the expert")

class SessionBooking(BaseModel):
    id: str = Field(..., description="Unique booking ID")
    room_id: str = Field(..., description="Unique WebRTC room identifier")
    expert: ExpertProfile
    applicant_name: str
    applicant_email: str
    scheduled_time: str
    status: str = Field(default="confirmed", description="Booking status: pending, confirmed, active, completed")
    created_at: str

class ExpertAIBriefing(BaseModel):
    candidate_name: str
    latest_job_title: Optional[str] = "Target Role"
    overall_match_score: Optional[float] = 0.0
    security_status: Optional[str] = "Verified Clean"
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    recommended_roadmap: List[Dict[str, Any]] = Field(default_factory=list)
    key_discussion_points: List[str] = Field(default_factory=list)
