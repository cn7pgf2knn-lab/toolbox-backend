"""
Users Routes
CRUD operations for users
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models
from app.auth import get_current_user, get_current_admin_user
from pydantic import BaseModel, EmailStr


router = APIRouter()


# Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
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


# Routes
@router.get("/", response_model=List[UserResponse])
async def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all users"""
    users = db.query(models.User).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get user by ID"""
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Update user (admin only)"""
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = user_data.username
    user.email = user_data.email
    user.name = user_data.name
    user.role = user_data.role

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Delete user (admin only)"""
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
