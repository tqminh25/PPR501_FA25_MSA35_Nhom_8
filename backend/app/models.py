from sqlalchemy import Column, Integer, String, Float, Date
from .db import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    student_code = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True)
    dob = Column(Date, nullable=True)
    home_town = Column(String, nullable=True)
    math_score = Column(Float, nullable=True)
    literature_score = Column(Float, nullable=True)
    english_score = Column(Float, nullable=True)