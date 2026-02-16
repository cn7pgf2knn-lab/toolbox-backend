"""
Database Models - SQLAlchemy ORM
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    """User model - Admin en werknemers"""
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String)
    role = Column(String, default="employee")  # admin, employee
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    completions = relationship("Completion", back_populates="user")


class Employee(Base):
    """Employee model - Werknemer details"""
    __tablename__ = "employees"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    job_function = Column(String)
    start_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    profile_image = Column(String)  # URL of base64
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    completions = relationship("Completion", back_populates="employee")


class Toolbox(Base):
    """Toolbox model - Toolbox talks/trainingen"""
    __tablename__ = "toolboxes"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)
    required = Column(Boolean, default=False)
    pdf_data = Column(Text)  # Base64 encoded PDF
    pdf_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    completions = relationship("Completion", back_populates="toolbox")


class Completion(Base):
    """Completion model - Voltooide toolboxen"""
    __tablename__ = "completions"

    id = Column(String, primary_key=True, index=True)
    employee_id = Column(String, ForeignKey("employees.id"), nullable=False)
    toolbox_id = Column(String, ForeignKey("toolboxes.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"))
    completed_date = Column(DateTime, default=datetime.utcnow)
    score = Column(Integer)
    notes = Column(Text)
    signature = Column(Text)  # Base64 encoded signature
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    employee = relationship("Employee", back_populates="completions")
    toolbox = relationship("Toolbox", back_populates="completions")
    user = relationship("User", back_populates="completions")


class Invitation(Base):
    """Invitation model - Uitnodigingen voor werknemers"""
    __tablename__ = "invitations"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=False)
    role = Column(String, default="employee")
    used = Column(Boolean, default=False)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class EmailConfig(Base):
    """Email Configuration - EmailJS config"""
    __tablename__ = "email_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(String)
    template_id = Column(String)
    public_key = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
