from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

app = FastAPI(title="Todo API", version="1.0.0")

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None , max_length=500)
    due_date: Optional[str] = Field(3, ge=1, le=5)
    priority: Optional[int] = Field(3, ge=1 , le=5)
    completed: Optional[bool] = False

@field_validator('title')
@classmethod
def title_must_be_trimmed(cls, v:str)->str:
    v=v.strip()
    if not v:
        raise ValueError('title cannot be empty or whitespace only')
    return v

@field_validator('description')
@classmethod
def validate_description(cls, v:Optional[str])-> Optional[str]:
    if v is not None:
        v = v.strip()
        if not v:
            return None
        return v
    
@field_validator('due_date')
