from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Any
from ..database import get_session
from ..services.auth_service import AuthService, UserCreate, UserLogin
from pydantic import BaseModel


router = APIRouter(prefix="/auth", tags=["Authentication"])


class TokenResponse(BaseModel):
    """Response model for token endpoints"""
    access_token: str
    token_type: str


@router.post("/register", response_model=TokenResponse)
def register_user(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user and return an access token
    """
    # Register the user
    user_data = AuthService.register_user(user_create, session)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed"
        )

    # Create access token
    access_token = AuthService.create_access_token_for_user(str(user_data["user_id"]))

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
def login_user(user_login: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticate user and return an access token
    """
    user_data = AuthService.authenticate_user(user_login.email, user_login.password, session)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = AuthService.create_access_token_for_user(str(user_data["user_id"]))

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout_user():
    """
    Logout user (stateless, so just client-side cleanup)
    """
    # Since JWT tokens are stateless, logout is handled client-side
    # by removing the token from client storage
    return {"message": "Successfully logged out"}