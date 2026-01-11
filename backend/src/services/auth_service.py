from typing import Optional
from sqlmodel import Session, select
from datetime import timedelta
from fastapi import HTTPException, status
from ..auth import create_access_token, create_refresh_token, verify_password
from ..models import User, UserCreate as UserCreateSchema, UserLogin as UserLoginSchema
from pydantic import BaseModel


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    email: str
    password: str


class UserLogin(BaseModel):
    """Schema for user login"""
    email: str
    password: str


class AuthService:
    """Service class to handle authentication-related operations"""

    @staticmethod
    def authenticate_user(email: str, password: str, session: Session) -> Optional[dict]:
        """
        Authenticate a user by email and password.
        """
        # Look up the user by email in the database
        user = session.exec(select(User).where(User.email == email)).first()

        if not user or not verify_password(password, user.hashed_password):
            return None

        return {
            "user_id": user.id,
            "email": user.email
        }

    @staticmethod
    def create_tokens_for_user(user_id: str) -> dict:
        """
        Create both access and refresh tokens for a user
        """
        access_token_expires = timedelta(minutes=30)
        refresh_token_expires = timedelta(days=7)

        access_token = create_access_token(
            data={"sub": user_id},
            expires_delta=access_token_expires
        )

        refresh_token = create_refresh_token(
            data={"sub": user_id},
            expires_delta=refresh_token_expires
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 1800  # 30 minutes in seconds
        }

    @staticmethod
    def refresh_access_token(refresh_token: str) -> Optional[dict]:
        """
        Refresh the access token using the refresh token
        """
        from ..auth import verify_token

        # Verify the refresh token
        payload = verify_token(refresh_token, expected_type="refresh")
        if not payload:
            return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        # Generate new access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user_id},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 1800  # 30 minutes in seconds
        }

    @staticmethod
    def register_user(user_create: UserCreate, session: Session) -> dict:
        """
        Register a new user.
        """
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        db_user = User(username=user_create.email.split('@')[0], email=user_create.email)
        db_user.set_password(user_create.password)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return {
            "user_id": db_user.id,
            "email": db_user.email
        }

    @staticmethod
    def create_access_token_for_user(user_id: str) -> str:
        """
        Create an access token for a user
        """
        from ..auth import create_access_token
        from datetime import timedelta

        access_token_expires = timedelta(minutes=30)
        return create_access_token(
            data={"sub": user_id},
            expires_delta=access_token_expires
        )