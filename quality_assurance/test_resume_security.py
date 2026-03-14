import pytest
from core_engine.resume_security.service import SecurityService
from fastapi import UploadFile
import io

@pytest.mark.asyncio
async def test_pii_redaction():
    service = SecurityService()
    
    # Test text with PII
    text = "John Doe is a software engineer at Google. Contact him at john.doe@example.com or +1-555-0199."
    entities = [
        ("John Doe", "PERSON"),
        ("john.doe@example.com", "EMAIL"),
        ("+1-555-0199", "PHONE"),
        ("Google", "ORG")
    ]
    
    redacted = service._redact_pii(text, entities)
    
    assert "John Doe" not in redacted
    assert "john.doe@example.com" not in redacted
    assert "+1-555-0199" not in redacted
    assert "Google" not in redacted
    
    assert "[PERSON]" in redacted
    assert "[EMAIL]" in redacted
    assert "[PHONE]" in redacted
    assert "[ORG]" in redacted
    
    print(f"Original: {text}")
    print(f"Redacted: {redacted}")

@pytest.mark.asyncio
async def test_detect_pii_basic():
    service = SecurityService()
    text = "My name is John Smith and I work at Microsoft. My email is john.smith@example.com."
    
    entities = service._detect_pii(text)
    
    labels = [e[1] for e in entities]
    assert "PERSON" in labels
    assert "EMAIL" in labels
    assert "ORG" in labels

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_detect_pii_basic())
    asyncio.run(test_pii_redaction())
