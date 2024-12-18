from pydantic import BaseModel, EmailStr, conint
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    is_admin: bool = False
    expires_in_days: Optional[int] = None
    preset_id: Optional[int] = None
    max_devices: conint(ge=1) = 1  # Default to 1 device

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    expires_in_days: Optional[int] = None
    preset_id: Optional[int] = None
    max_devices: Optional[conint(ge=1)] = None

class UserResponse(UserBase):
    is_admin: bool
    created_at: datetime
    expires_at: Optional[datetime] = None
    preset_id: Optional[int] = None
    max_devices: int = 1  # Add default value
    active_sessions: int = 0
    is_active: bool = True
    assigned_accounts: List[int] = []

    class Config:
        from_attributes = True