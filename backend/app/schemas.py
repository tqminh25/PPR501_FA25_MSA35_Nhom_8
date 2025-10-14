from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class StudentIn(BaseModel):
    student_code: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    dob: Optional[date] = None  # yyyy-mm-dd
    home_town: Optional[str] = None
    math_score: Optional[float] = Field(None, ge=0, le=10)
    literature_score: Optional[float] = Field(None, ge=0, le=10)
    english_score: Optional[float] = Field(None, ge=0, le=10)

class StudentOut(StudentIn):
    id: int
    class Config:
        orm_mode = True

class StudentGradesUpdate(BaseModel):
    """Schema cho việc cập nhật điểm số"""
    math_score: Optional[float] = Field(None, ge=0, le=10)
    literature_score: Optional[float] = Field(None, ge=0, le=10)
    english_score: Optional[float] = Field(None, ge=0, le=10)