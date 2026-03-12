from fastapi import APIRouter, HTTPException
from core_engine.smart_match.schemas import SmartMatchRequest, SmartMatchResponse
from core_engine.smart_match.service import smart_match_service

router = APIRouter()

@router.post("/match", response_model=SmartMatchResponse)
async def match_resume_to_jd(request: SmartMatchRequest):
    """
    Analyzes the resume text against the job description text and returns 
    a match score, matched skills, missing skills, and justification.
    """
    try:
        match_result = await smart_match_service.calculate_match(request)
        return match_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
