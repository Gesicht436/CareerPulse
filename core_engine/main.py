import re
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core_engine.smart_match.router import router as smart_match_router
from core_engine.resume_security.router import router as security_router
from core_engine.expert_session.router import router as expert_router
from core_engine.auth.router import router as auth_router
from core_engine.admin.router import router as admin_router
from core_engine.resume_security.service import security_service
from core_engine.smart_match.service import smart_match_service
from core_engine.telemetry.service import telemetry_service

app = FastAPI(
    title="CareerPulse Core Engine",
    description="The central nervous system of CareerPulse, handling user authentication, admin control, telemetry analytics, matching, data, and live expert interactions.",
    version="0.2.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def telemetry_and_maintenance_middleware(request: Request, call_next):
    # Check maintenance mode for non-admin requests
    path = request.url.path
    if not path.startswith("/api/v1/admin") and not path == "/":
        settings = telemetry_service.get_settings()
        if settings.get("maintenance_mode", False):
            return JSONResponse(
                status_code=503,
                content={"detail": "CareerPulse is currently undergoing scheduled maintenance. Please check back shortly."}
            )

    response = await call_next(request)
    
    # Log page view telemetry for root/frontend navigation requests
    if request.method == "GET" and (path == "/" or path.endswith(".html")):
        telemetry_service.log_event("PAGE_VIEW", f"Page view recorded for {path}", {"path": path})
        
    return response

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin Controls & Telemetry"])
app.include_router(security_router, prefix="/api/v1/security", tags=["Security"])
app.include_router(smart_match_router, prefix="/api/v1/smart-match", tags=["Smart Match"])
app.include_router(expert_router, prefix="/api/v1/expert", tags=["Expert Interaction"])

@app.post("/api/v1/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    """
    Unified endpoint to upload, extract text, and match a resume.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        # Check if uploads are enabled
        settings = telemetry_service.get_settings()
        if not settings.get("enable_resume_upload", True):
            raise HTTPException(status_code=403, detail="Resume upload feature is temporarily disabled by administrator.")

        # 1. Extract raw text from resume
        security_result = await security_service.process_resume(file)
        resume_text = security_result["redacted_text"]

        # Extract educational qualification from resume text
        qual_patterns = [
            (r'\b(b\.?tech|b\.?e\.?|bachelor of technology|bachelor of engineering)\b', "B.Tech / B.E."),
            (r'\b(m\.?tech|m\.?e\.?|master of technology)\b', "M.Tech"),
            (r'\b(b\.?sc|bachelor of science)\b', "B.Sc"),
            (r'\b(m\.?sc|master of science)\b', "M.Sc"),
            (r'\b(bca|bachelor of computer applications)\b', "BCA"),
            (r'\b(mca|master of computer applications)\b', "MCA"),
            (r'\b(b\.?com|bachelor of commerce)\b', "B.Com"),
            (r'\b(mba|master of business administration)\b', "MBA"),
            (r'\b(ph\.?d|doctor of philosophy)\b', "Ph.D")
        ]
        
        detected_qualification = "B.Tech / B.E."
        text_lower = resume_text.lower()
        for pat, name in qual_patterns:
            if re.search(pat, text_lower):
                detected_qualification = name
                break

        # 2. Match with Smart Match Service for top 5 recommendations with strict qualification filter
        match_results = await smart_match_service.match_against_database(
            resume_text, 
            limit=5, 
            qualification=detected_qualification, 
            strict_qualification=True
        )

        all_matches = match_results.top_matches if match_results.top_matches else []
        top_match = all_matches[0] if all_matches else None
        
        # 3. Log Telemetry Event
        score = 0
        if top_match:
            if hasattr(top_match, "match_details") and top_match.match_details:
                score = getattr(top_match.match_details, "overall_score", 0)
            elif isinstance(top_match, dict):
                score = top_match.get("match_details", {}).get("overall_score", 0)
        
        telemetry_service.log_event(
            "RESUME_ANALYSIS",
            f"Processed PDF resume '{file.filename}' for '{detected_qualification}' qualification with top match score {round(score)}%.",
            {"filename": file.filename, "qualification": detected_qualification, "overall_score": score, "total_recommendations": len(all_matches)}
        )

        # 4. Combine results with top 5 recommendations and qualification metadata
        return {
            "filename": file.filename,
            "qualification": detected_qualification,
            "security_report": security_result["security_report"],
            "top_matches": all_matches,
            "analysis": top_match
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to CareerPulse Core Engine API with Telemetry Analytics"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
