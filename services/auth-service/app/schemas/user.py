from pydantic import BaseModel, EmailStr
from datetime import datetime

# Base schema for user properties
class UserBase(BaseModel):
    email: EmailStr

# Schema for creating a new user (request)
class UserCreate(UserBase):
    password: str

# Schema for reading user data (response)
class UserPublic(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True # Pydantic v2