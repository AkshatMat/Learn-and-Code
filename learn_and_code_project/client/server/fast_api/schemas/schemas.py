from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Literal
from uuid import UUID

class SignUpParams(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
        description="Username must be 3-50 characters long and can only contain letters, numbers, and underscores."
    )
    
    email: EmailStr = Field(
        description="A valid email address."
    )

    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must be 8-128 characters long and include at least one lowercase letter, one uppercase letter, one number, and one special character."
    )
    
    role: Literal["User"] = Field(
        default="User", description="Role is fixed as 'User'."
    )
    
    @field_validator('username')
    def no_whitespace_in_username(cls, value):
        if any(char.isspace() for char in value):
            raise ValueError("Username must not contain any whitespace.")
        return value
    
class LogInParams(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
        description="Username must be 3-50 characters long."
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must be 8-128 characters long."
    )
    @field_validator('username')
    def no_whitespace_in_username(cls, value):
        if any(char.isspace() for char in value):
            raise ValueError("Username must not contain any whitespace.")
        return value