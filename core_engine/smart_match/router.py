from fastapi import APIRouter, HTTPException
from core_engine.smart_match.schemas import SmartMatchRequest, SmartMatchResponse, MultiJobMatchResponse
from core_engine.smart_match.service import smart_match_service

router = APIRouter()

@router.post("/match-all", response_model=MultiJobMatchResponse)
async def match_resume_to_all_jobs(resume_text: str, limit: int = 5):
    """
    Takes a resume text and finds the most relevant jobs from the 1.61M jobs database,
    providing a detailed match report for each.
    """
    try:
        results = await smart_match_service.match_against_database(resume_text, limit=limit)
        return results
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/match", response_model=SmartMatchResponse)
async def match_resume_to_jd(request: SmartMatchRequest):
    """
    Analyzes the resume text against the job description text and returns 
    a match score, matched skills, missing skills, and justification.
    """
    try:
        from core_engine.telemetry.service import telemetry_service
        settings = telemetry_service.get_settings()
        if not settings.get("enable_jd_analyzer", True):
            raise HTTPException(status_code=403, detail="Custom JD Analyzer feature is temporarily disabled by administrator.")

        match_result = await smart_match_service.calculate_match(request)
        telemetry_service.log_event("JD_ANALYZED", f"Custom JD match evaluated with score {round(match_result.overall_score)}%.", {"overall_score": match_result.overall_score})
        return match_result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search-jobs")
async def search_jobs(query: str, limit: int = 5, experience_level: str = None):
    """
    Smart search for specific jobs with optional filtering.
    """
    try:
        from core_engine.data_layer.service import data_layer_service
        from core_engine.telemetry.service import telemetry_service
        results = data_layer_service.search_jobs(query, limit=limit, experience_level=experience_level)
        telemetry_service.log_event("JOB_SEARCH", f"Executed natural language job query: '{query}'.", {"query": query, "results_count": len(results)})
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
