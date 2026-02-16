from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

# ==================== USER SCHEMAS ====================

class UserBase(BaseModel):
    email: EmailStr
    name: str
    is_admin: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # Pydantic 1.x style

class User(UserInDB):
    pass

# ==================== AUTH SCHEMAS ====================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ==================== EMPLOYEE SCHEMAS ====================

class EmployeeBase(BaseModel):
    name: str
    employee_number: str
    department: Optional[str] = None
    position: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    employee_number: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None

class EmployeeInDB(EmployeeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Employee(EmployeeInDB):
    pass

# ==================== TOOLBOX SCHEMAS ====================

class ToolboxBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    items: List[str] = []

    @validator('items', pre=True)
    def parse_items(cls, v):
        if isinstance(v, str):
            import json
            return json.loads(v)
        return v

class ToolboxCreate(ToolboxBase):
    pass

class ToolboxUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    items: Optional[List[str]] = None

class ToolboxInDB(ToolboxBase):
    id: int
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True

class Toolbox(ToolboxInDB):
    pass

# ==================== COMPLETION SCHEMAS ====================

class CompletionBase(BaseModel):
    toolbox_id: int
    employee_id: int
    completed_items: List[str] = []
    notes: Optional[str] = None

    @validator('completed_items', pre=True)
    def parse_completed_items(cls, v):
        if isinstance(v, str):
            import json
            return json.loads(v)
        return v

class CompletionCreate(CompletionBase):
    pass

class CompletionUpdate(BaseModel):
    completed_items: Optional[List[str]] = None
    notes: Optional[str] = None

class CompletionInDB(CompletionBase):
    id: int
    completed_at: datetime
    synced: bool = False

    class Config:
        orm_mode = True

class Completion(CompletionInDB):
    pass
