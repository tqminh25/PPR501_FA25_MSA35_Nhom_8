from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas

def list_students(db: Session, skip=0, limit=100, search: str | None = None):
    q = db.query(models.Student)
    if search:
        like = f"%{search}%"
        q = q.filter(or_(
            models.Student.student_code.ilike(like),
            models.Student.first_name.ilike(like),
            models.Student.last_name.ilike(like),
            models.Student.email.ilike(like),
        ))
    return q.offset(skip).limit(limit).all()

def get_student(db: Session, id: int):
    return db.query(models.Student).get(id)

def create_student(db: Session, data: schemas.StudentIn):
    if db.query(models.Student).filter_by(student_code=data.student_code).first():
        raise ValueError("student_code exists")
    if data.email and db.query(models.Student).filter_by(email=data.email).first():
        raise ValueError("email exists")
    obj = models.Student(**data.dict())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def update_student(db: Session, id: int, data: schemas.StudentIn):
    obj = get_student(db, id)
    if not obj: return None
    if data.student_code != obj.student_code and \
       db.query(models.Student).filter_by(student_code=data.student_code).first():
        raise ValueError("student_code exists")
    if data.email and data.email != obj.email and \
       db.query(models.Student).filter_by(email=data.email).first():
        raise ValueError("email exists")
    for k, v in data.dict().items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

def delete_student(db: Session, id: int):
    obj = get_student(db, id)
    if not obj: return False
    db.delete(obj); db.commit()
    return True