import uuid
from typing import List, Dict, Optional
from datetime import datetime
from core_engine.expert_session.schemas import ExpertProfile, SessionBooking, BookingRequest, ExpertAIBriefing

# In-memory store for demonstration and fast iteration
MOCK_EXPERTS: List[ExpertProfile] = [
    ExpertProfile(
        id="exp-101",
        name="Alex Rivera",
        title="Principal AI Architect",
        company="DeepMind / Google",
        domain="Artificial Intelligence & ML Systems",
        bio="12+ years building distributed AI platforms, LLM quantization pipelines, and local RAG systems.",
        rating=4.95,
        total_sessions=142,
        avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
    ),
    ExpertProfile(
        id="exp-102",
        name="Dr. Elena Rostova",
        title="Staff Security Engineer",
        company="CrowdStrike",
        domain="Cybersecurity & Defensive Audit",
        bio="Specializes in adversarial LLM defense, document security auditing, and zero-trust infrastructure.",
        rating=4.98,
        total_sessions=98,
        avatar_url="https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150"
    ),
    ExpertProfile(
        id="exp-103",
        name="Marcus Vance",
        title="VP of Engineering",
        company="Stripe",
        domain="Full-Stack Engineering & Scalable Systems",
        bio="Helping senior engineers transition to staff/principal roles and master technical system design interviews.",
        rating=4.92,
        total_sessions=210,
        avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150"
    )
]

BOOKINGS_STORE: Dict[str, SessionBooking] = {}

class ExpertSessionService:
    def get_all_experts(self) -> List[ExpertProfile]:
        return MOCK_EXPERTS

    def get_expert_by_id(self, expert_id: str) -> Optional[ExpertProfile]:
        for expert in MOCK_EXPERTS:
            if expert.id == expert_id:
                return expert
        return None

    def create_booking(self, req: BookingRequest) -> SessionBooking:
        expert = self.get_expert_by_id(req.expert_id)
        if not expert:
            raise ValueError(f"Expert with ID '{req.expert_id}' not found.")
        
        booking_id = f"book-{str(uuid.uuid4())[:8]}"
        room_id = f"room-{str(uuid.uuid4())[:12]}"
        
        booking = SessionBooking(
            id=booking_id,
            room_id=room_id,
            expert=expert,
            applicant_name=req.applicant_name,
            applicant_email=req.applicant_email,
            scheduled_time=req.scheduled_time,
            status="confirmed",
            created_at=datetime.utcnow().isoformat()
        )
        
        BOOKINGS_STORE[booking_id] = booking
        BOOKINGS_STORE[room_id] = booking # Map room_id as well for fast retrieval
        return booking

    def get_booking(self, identifier: str) -> Optional[SessionBooking]:
        return BOOKINGS_STORE.get(identifier)

    def generate_ai_briefing(self, candidate_name: str, analysis_data: Optional[Dict] = None) -> ExpertAIBriefing:
        """
        Synthesizes the candidate's CareerPulse resume audit, SBERT match score, 
        and Qwen LLM roadmap into a structured dossier for the industry expert.
        """
        if not analysis_data or "analysis" not in analysis_data:
            raise ValueError(
                "Cannot generate AI Expert Briefing Dossier without valid resume analysis data. "
                "Please analyze a resume first."
            )

        analysis = analysis_data.get("analysis", {})
        match_details = analysis.get("match_details", {})
        sec_report = analysis_data.get("security_report", {})

        is_safe = sec_report.get("is_safe", True)
        sec_status = "Verified Clean" if is_safe else "Flagged - Review Required"

        matched = match_details.get("matched_skills", [])
        missing = match_details.get("missing_skills", [])
        roadmap = match_details.get("career_roadmap", [])

        discussion_points = [
            f"Candidate achieved an overall ATS match score of {match_details.get('overall_score', 0)}%.",
            f"Discuss strategy for closing key skill gaps: {', '.join(missing[:3]) if missing else 'None detected'}.",
            "Review candidate's tailored weekly learning roadmap and refine timelines."
        ]

        return ExpertAIBriefing(
            candidate_name=candidate_name,
            latest_job_title=analysis.get("job_title", "Target Role"),
            overall_match_score=match_details.get("overall_score", 0.0),
            security_status=sec_status,
            matched_skills=matched,
            missing_skills=missing,
            recommended_roadmap=roadmap,
            key_discussion_points=discussion_points
        )

expert_session_service = ExpertSessionService()
