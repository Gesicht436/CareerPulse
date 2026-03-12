import pytest
from core_engine.smart_match.service import smart_match_service
from core_engine.smart_match.schemas import SmartMatchRequest

@pytest.mark.asyncio
async def test_calculate_match_real_embedding():
    # Setup real request
    request = SmartMatchRequest(
        resume_text="Experienced Python developer with FastAPI expertise and Docker knowledge.",
        jd_text="Looking for a Python developer with FastAPI and Docker experience."
    )
    
    # Call the service
    response = await smart_match_service.calculate_match(request)
    
    # Assertions
    # We expect a high score for very similar text
    assert response.overall_score > 80.0
    assert len(response.justification) > 0
    assert len(response.recommendations) > 0
    print(f"Match Score: {response.overall_score}%")

@pytest.mark.asyncio
async def test_calculate_match_dissimilar():
    # Setup dissimilar request
    request = SmartMatchRequest(
        resume_text="Professional chef with 10 years of experience in Italian cuisine.",
        jd_text="Looking for a Python developer with FastAPI and Docker experience."
    )
    
    # Call the service
    response = await smart_match_service.calculate_match(request)
    
    # Assertions
    # We expect a low score for unrelated text
    assert response.overall_score < 40.0
    print(f"Dissimilar Match Score: {response.overall_score}%")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_calculate_match_real_embedding())
    asyncio.run(test_calculate_match_dissimilar())
