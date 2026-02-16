"""
Completions Routes
Track toolbox completions by employees
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from app.database import get_db
from app import models
from app.auth import get_current_user
from pydantic import BaseModel


router = APIRouter()


# Schemas
class CompletionCreate(BaseModel):
    employee_id: str
    toolbox_id: str
    score: int = None
    notes: str = None
    signature: str = None


class CompletionResponse(BaseModel):
    id: str
    employee_id: str
    toolbox_id: str
    user_id: str = None
    completed_date: datetime
    score: int = None
    notes: str = None

    class Config:
        from_attributes = True


# Routes
@router.get("/", response_model=List[CompletionResponse])
async def get_completions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all completions"""
    completions = db.query(models.Completion).all()
    return completions


@router.post("/", response_model=CompletionResponse)
async def create_completion(
    completion_data: CompletionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create new completion"""
    # Verify employee exists
    employee = db.query(models.Employee).filter(
        models.Employee.id == completion_data.employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Verify toolbox exists
    toolbox = db.query(models.Toolbox).filter(
        models.Toolbox.id == completion_data.toolbox_id
    ).first()

    if not toolbox:
        raise HTTPException(status_code=404, detail="Toolbox not found")

    # Create completion
    new_completion = models.Completion(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        **completion_data.dict()
    )

    db.add(new_completion)
    db.commit()
    db.refresh(new_completion)

    return new_completion


@router.get("/employee/{employee_id}", response_model=List[CompletionResponse])
async def get_employee_completions(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all completions for specific employee"""
    completions = db.query(models.Completion).filter(
        models.Completion.employee_id == employee_id
    ).all()

    return completions
