"""
Employees Routes
CRUD operations for employees
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database import get_db
from app import models
from app.auth import get_current_user, get_current_admin_user
from pydantic import BaseModel, EmailStr
from datetime import datetime


router = APIRouter()


# Schemas
class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    job_function: str = None
    start_date: datetime = None
    profile_image: str = None


class EmployeeResponse(BaseModel):
    id: str
    name: str
    email: str
    job_function: str = None
    start_date: datetime = None
    is_active: bool
    profile_image: str = None

    class Config:
        from_attributes = True


# Routes
@router.get("/", response_model=List[EmployeeResponse])
async def get_employees(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all employees"""
    employees = db.query(models.Employee).all()
    return employees


@router.post("/", response_model=EmployeeResponse)
async def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Create new employee (admin only)"""
    # Check if employee with email exists
    existing = db.query(models.Employee).filter(models.Employee.email == employee_data.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Employee with this email already exists")

    new_employee = models.Employee(
        id=str(uuid.uuid4()),
        **employee_data.dict()
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get employee by ID"""
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: str,
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Update employee (admin only)"""
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in employee_data.dict().items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """Delete employee (admin only)"""
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}
