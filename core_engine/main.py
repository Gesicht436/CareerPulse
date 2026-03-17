from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core_engine.smart_match.router import router as smart_match_router
from core_engine.resume_security.router import router as security_router

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

@app.get("/")
async def root():
    return {"message": "Welcome to CareerPulse Core Engine API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
