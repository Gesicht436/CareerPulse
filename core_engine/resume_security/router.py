from fastapi import APIRouter, UploadFile, File, HTTPException
from core_engine.resume_security.service import security_service
from typing import Dict, Any

router = APIRouter()

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Securely uploads a resume PDF, extracts text, and performs security audits.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        result = await security_service.process_resume(file)
        
        # If the file is not safe, we still return the report but might 
        # want to prevent further processing in a real-world scenario.
        return result
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
