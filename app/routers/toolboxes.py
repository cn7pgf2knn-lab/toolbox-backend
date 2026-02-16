"""
Toolboxes Routes
CRUD operations for toolboxes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database import get_db
from app import models
from app.auth import get_current_user, get_current_admin_user
from pydantic import BaseModel


router = APIRouter()


# Schemas
class ToolboxCreate(BaseModel):
    title: str
    description: str = None
    category: str = None
    required: bool = False
    pdf_data: str = None
    pdf_name: str = None


class ToolboxResponse(BaseModel):
    id: str
    title: str
    description: str = None
    category: str = None
    required: bool
    pdf_name: str = None

    class Config:
        from_attributes = True


# Routes
@router.get("/", response_model=List[ToolboxResponse])
async def get_toolboxes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all toolboxes"""
    toolboxes = db.query(models.Toolbox).all()
    return toolboxes


@router.post("/", response_model=ToolboxResponse)
async def create_toolbox(
    toolbox_data: ToolboxCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Create new toolbox (admin only)"""
    new_toolbox = models.Toolbox(
        id=str(uuid.uuid4()),
        **toolbox_data.dict()
    )

    db.add(new_toolbox)
    db.commit()
    db.refresh(new_toolbox)

    return new_toolbox


@router.get("/{toolbox_id}")
async def get_toolbox(
    toolbox_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get toolbox by ID (including PDF data)"""
    toolbox = db.query(models.Toolbox).filter(models.Toolbox.id == toolbox_id).first()

    if not toolbox:
        raise HTTPException(status_code=404, detail="Toolbox not found")

    return toolbox


@router.delete("/{toolbox_id}")
async def delete_toolbox(
    toolbox_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Delete toolbox (admin only)"""
    toolbox = db.query(models.Toolbox).filter(models.Toolbox.id == toolbox_id).first()

    if not toolbox:
        raise HTTPException(status_code=404, detail="Toolbox not found")

    db.delete(toolbox)
    db.commit()

    return {"message": "Toolbox deleted successfully"}
