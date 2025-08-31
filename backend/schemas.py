from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    phone: Optional[str] = None
    department: Optional[str] = None
    status: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    status: Optional[str] = None

class EmployeeOut(EmployeeBase):
    id: int
    class Config:
        from_attributes = True

class PaginatedEmployees(BaseModel):
    items: List[EmployeeOut]
    total: int
    page: int
    page_size: int
