from typing import Literal
from pydantic import BaseModel, EmailStr, Field

class AdminCreateUserRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Literal["admin", "user"] = "user"

class UserStatusUpdate(BaseModel):
    is_active: bool