from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..db import SessionLocal, Base, engine
from .. import schemas, crud

Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/students", tags=["students"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("", response_model=list[schemas.StudentOut])
def list_students(skip: int = 0, limit: int = 100, search: str | None = Query(None), db: Session = Depends(get_db)):
    return crud.list_students(db, skip, limit, search)

@router.get("/{id}", response_model=schemas.StudentOut)
def get_student(id: int, db: Session = Depends(get_db)):
    obj = crud.get_student(db, id)
    if not obj: raise HTTPException(404, "Not found")
    return obj

@router.post("", response_model=schemas.StudentOut, status_code=201)
def create_student(payload: schemas.StudentIn, db: Session = Depends(get_db)):
    try:
        return crud.create_student(db, payload)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.put("/{id}", response_model=schemas.StudentOut)
def update_student(id: int, payload: schemas.StudentIn, db: Session = Depends(get_db)):
    obj = crud.update_student(db, id, payload)
    if not obj: raise HTTPException(404, "Not found")
    return obj

@router.delete("/{id}", status_code=204)
def delete_student(id: int, db: Session = Depends(get_db)):
    ok = crud.delete_student(db, id)
    if not ok: raise HTTPException(404, "Not found")

@router.get("/by-code/{student_code}", response_model=schemas.StudentOut)
def get_student_by_code(student_code: str, db: Session = Depends(get_db)):
    obj = db.query(crud.models.Student).filter(crud.models.Student.student_code == student_code).first()
    if not obj:
        raise HTTPException(404, "Not found")
    return obj

@router.patch("/by-code/{student_code}/grades", response_model=schemas.StudentOut)
def update_student_grades(student_code: str, grades: schemas.StudentGradesUpdate, db: Session = Depends(get_db)):
    """Cập nhật điểm số của học sinh theo mã học sinh"""
    student = db.query(crud.models.Student).filter(crud.models.Student.student_code == student_code).first()
    if not student:
        raise HTTPException(404, "Student not found")
    
    # Cập nhật điểm số
    if grades.math_score is not None:
        student.math_score = grades.math_score
    if grades.literature_score is not None:
        student.literature_score = grades.literature_score
    if grades.english_score is not None:
        student.english_score = grades.english_score
    
    db.commit()
    db.refresh(student)
    return student