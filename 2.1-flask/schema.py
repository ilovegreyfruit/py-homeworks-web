from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class AdCreateSchema(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    owner: str = Field(..., min_length=1)


class AdSchema(AdCreateSchema):
    id: int
    created_at: datetime