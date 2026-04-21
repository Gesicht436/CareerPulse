from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core_engine.smart_match.router import router as smart_match_router
from core_engine.resume_security.router import router as security_router
from core_engine.resume_security.service import security_service
from core_engine.smart_match.service import smart_match_service

app = FastAPI(
    title="CareerPulse Core Engine",
    description="The central nervous system of CareerPulse, handling security, matching, and data.",
    version="0.1.0",
)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(security_router, prefix="/api/v1/security", tags=["Security"])
app.include_router(smart_match_router, prefix="/api/v1/smart-match", tags=["Smart Match"])

@app.post("/api/v1/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    """
    Unified endpoint to securely upload, audit, and match a resume.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        # 1. Process with Security Service (Extraction + Redaction + Audit)
        security_result = await security_service.process_resume(file)
        
        # 2. Match with Smart Match Service
        # We use the redacted text for matching to maintain privacy
        match_results = await smart_match_service.match_against_database(
            security_result["redacted_text"], limit=1
        )
        
        # 3. Combine results
        return {
            "filename": file.filename,
            "security_report": security_result["security_report"],
            "analysis": match_results.top_matches[0] if match_results.top_matches else None
        }
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to CareerPulse Core Engine API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
