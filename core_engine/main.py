from fastapi import FastAPI
from core_engine.smart_match.router import router as smart_match_router

app = FastAPI(
    title="CareerPulse Core Engine",
    description="The central nervous system of CareerPulse, handling security, matching, and data.",
    version="0.1.0",
)

# Include routers
app.include_router(smart_match_router, prefix="/api/v1/smart-match", tags=["Smart Match"])

@app.get("/")
async def root():
    return {"message": "Welcome to CareerPulse Core Engine API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
