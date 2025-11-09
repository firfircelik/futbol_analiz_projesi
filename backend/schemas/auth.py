"""
Authentication schemas
"""
from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """Request schema for user signup"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = None


class LoginRequest(BaseModel):
    """Request schema for user login"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response schema for authentication token"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
