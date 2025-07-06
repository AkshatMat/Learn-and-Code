from pydantic import BaseModel, Field, field_validator
from typing import Literal

class APIUpsertRequest(BaseModel):
    api_url: str = Field(
        min_length=1,
        description="API URL must not be empty"
    )
    status: Literal["Active", "Inactive", "Maintenance", "active", "inactive", "maintenance"] = Field(
        default="Active",
        description="API status"
    )
    api_key: str = Field(
        min_length=1,
        description="API key must not be empty"
    )
    name: str = Field(
        min_length=1,
        max_length=100,
        description="API name must be 1-100 characters long"
    )

    @field_validator('api_url')
    def validate_api_url(cls, value):
        if not value.startswith(('http://', 'https://')):
            raise ValueError("API URL must start with http:// or https://")
        return value

    @field_validator('name')
    def validate_name(cls, value):
        if any(char.isspace() for char in value):
            raise ValueError("API name must not contain any whitespace")
        return value

class APIStatusRequest(BaseModel):
    api_name: str = Field(
        min_length=1,
        max_length=100,
        description="API name must be 1-100 characters long"
    )
    status: Literal["Active", "Inactive", "Maintenance", "active", "inactive", "maintenance"] = Field(
        description="New API status"
    )

    @field_validator('api_name')
    def validate_api_name(cls, value):
        if any(char.isspace() for char in value):
            raise ValueError("API name must not contain any whitespace")
        return value

class APIDeleteRequest(BaseModel):
    api_url: str = Field(
        min_length=1,
        description="API URL to delete"
    )

    @field_validator('api_url')
    def validate_api_url(cls, value):
        if not value.startswith(('http://', 'https://')):
            raise ValueError("API URL must start with http:// or https://")
        return value 