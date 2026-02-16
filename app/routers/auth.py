"""
Authentication Routes
Login, register, token management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import uuid

from app.database import get_db
from app import models
from app.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user
)
from app.config import settings
from pydantic import BaseModel, EmailStr


router = APIRouter()


# Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str
    role: str = "employee"


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# Routes
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register new user
    """
    # Check if user exists
    existing_user = db.query(models.User).filter(
        (models.User.username == user_data.username) | (models.User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # Create new user
    new_user = models.User(
        id=str(uuid.uuid4()),
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        name=user_data.name,
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with username/email and password
    Returns JWT access token
    """
    # Find user by username or email
    user = db.query(models.User).filter(
        (models.User.username == form_data.username) | (models.User.email == form_data.username)
    ).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "username": user.username, "role": user.role},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    """
    Get current logged in user information
    """
    return current_user


@router.post("/logout")
async def logout(current_user: models.User = Depends(get_current_user)):
    """
    Logout (client should discard token)
    """
    return {"message": "Successfully logged out"}
