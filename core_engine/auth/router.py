from fastapi import APIRouter, HTTPException, Header, Depends
from core_engine.auth.schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from core_engine.auth.service import auth_service
from typing import Optional

router = APIRouter()

@router.post("/signup", response_model=TokenResponse)
async def signup(data: UserCreate):
    """
    Registers a new user account with email and password.
    """
    try:
        user_resp, token = auth_service.signup(data)
        return TokenResponse(access_token=token, token_type="bearer", user=user_resp)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration error: {str(e)}")

@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    """
    Authenticates a user and returns a session JWT token.
    """
    try:
        user_resp, token = auth_service.login(data)
        return TokenResponse(access_token=token, token_type="bearer", user=user_resp)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

@router.get("/me", response_model=UserResponse)
async def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Returns the authenticated user's profile information.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header.")
    
    token = authorization.split(" ")[1]
    user = auth_service.get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired session token.")
    
    return user
