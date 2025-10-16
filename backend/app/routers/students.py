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

@router.get("/statistics", response_model=dict)
def get_students_statistics(db: Session = Depends(get_db)):
    """Lấy thống kê tổng quan về học sinh"""
    # Lấy tất cả học sinh
    all_students = db.query(crud.models.Student).all()
    
    if not all_students:
        return {
            "total_students": 0,
            "avg_math_score": 0.0,
            "avg_literature_score": 0.0,
            "avg_english_score": 0.0,
            "avg_overall_score": 0.0
        }
    
    # Tính tổng số học sinh
    total_students = len(all_students)
    
    # Tính điểm trung bình các môn
    math_scores = []
    literature_scores = []
    english_scores = []
    overall_scores = []
    
    for student in all_students:
        # Lọc điểm hợp lệ (0-10)
        if student.math_score is not None and 0 <= student.math_score <= 10:
            math_scores.append(student.math_score)
        if student.literature_score is not None and 0 <= student.literature_score <= 10:
            literature_scores.append(student.literature_score)
        if student.english_score is not None and 0 <= student.english_score <= 10:
            english_scores.append(student.english_score)
        
        # Tính điểm trung bình của từng học sinh (chỉ với điểm hợp lệ)
        student_scores = []
        if student.math_score is not None and 0 <= student.math_score <= 10:
            student_scores.append(student.math_score)
        if student.literature_score is not None and 0 <= student.literature_score <= 10:
            student_scores.append(student.literature_score)
        if student.english_score is not None and 0 <= student.english_score <= 10:
            student_scores.append(student.english_score)
        
        if student_scores:
            avg_student = sum(student_scores) / len(student_scores)
            overall_scores.append(avg_student)
    
    # Tính điểm trung bình
    avg_math = sum(math_scores) / len(math_scores) if math_scores else 0.0
    avg_literature = sum(literature_scores) / len(literature_scores) if literature_scores else 0.0
    avg_english = sum(english_scores) / len(english_scores) if english_scores else 0.0
    avg_overall = sum(overall_scores) / len(overall_scores) if overall_scores else 0.0
    
    return {
        "total_students": total_students,
        "avg_math_score": round(avg_math, 2),
        "avg_literature_score": round(avg_literature, 2),
        "avg_english_score": round(avg_english, 2),
        "avg_overall_score": round(avg_overall, 2)
    }

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