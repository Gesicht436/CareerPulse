from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, json_schema_extra={"example": "Jane Doe"})
    email: str = Field(..., json_schema_extra={"example": "jane@example.com"})
    password: str = Field(..., min_length=6, json_schema_extra={"example": "password123"})

class UserLogin(BaseModel):
    email: str = Field(..., json_schema_extra={"example": "jane@example.com"})
    password: str = Field(..., json_schema_extra={"example": "password123"})

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    created_at: str
    role: str = "user"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
