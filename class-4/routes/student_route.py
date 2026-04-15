from services.student_services import create_student, put_update_student
from model.student_model import StudentCreate, Students
from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import  select
from sqlalchemy.exc import IntegrityError
from database.db import get_session

router = APIRouter()

@router.get("/student")
def get_student_list(session=Depends(get_session)):
    result = session.exec(select(Students)).all()
    return result

@router.get("/students")
def search_students(name:str , session=Depends(get_session)):
    query = session.query(Students)
    if name:
        query = query.filter(Students.name.ilike(f"%{name}%"))

@router.get("/student/{student_id}")
def get_student(student_id:int , session=Depends(get_session)):
    result = session.get(Students , student_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student not Found!")
    return result

@router.post("/student")
def post_student(student: StudentCreate, session=Depends(get_session)):
    student_data = Students(**student.model_dump())
    # std = student.model_dump()
    # print(std)
    # student_data = Students(name=student.name , email=student.email, roll_number=student.roll_number , phone_number=student.phone_number)
    result = create_student(session, student_data)
    return result

@router.put("/student/{student_id}")
def put_student(student_id:int, student:Students, session=Depends(get_session)):
    # ⚠ WARNING: Ensure argument order matches put_update_student(session, student_id, student)
    # Mismatched order previously caused a 500 error (Students object passed as primary key)
    result = put_update_student(session, student_id, student)
    return result
    
@router.patch("/student/{student_id}")
def patch_student(student_id:int, student: Students, session=Depends(get_session)):
    """Partially update a student (only provided fields)"""
    try: 
        db_student = session.get(Students, student_id)
        if not db_student:
            raise HTTPException(status_code=404, detail="Student Not Found!")
        
        data_student = student.model_dump(exclude_unset=True)
        for key, value in data_student.items():
            if value is not None:
                setattr(db_student , key , value)

        session.add(db_student)
        session.commit()
        session.refresh(db_student)
        return db_student
        
    except IntegrityError as ex:
        session.rollback()
        return {"detail": "Roll Number or Email is Duplicate"}
        
        
@router.delete("/student/{student_id}")
def deleted_student(student_id: int, session=Depends(get_session)):
    """Delete a Student by ID"""
    try:
        db_student = session.get(Students, student_id)
        if not db_student:
            raise HTTPException(status_code=404, detail="Student Not Found!")
        
        session.delete(db_student)
        session.commit()
        return {"detail": f"Student with ID {student_id} deleted successfully!"}
    
    except IntegrityError as ex:
        session.rollback()
        return {"detail":"Error while deleting students"}



# ═════════════════════════════════════════════════════════════════════════════
# HTTP METHODS SUMMARY:
# ═════════════════════════════════════════════════════════════════════════════
# 
# GET    /student           → Retrieve all students          ✓ IMPLEMENTED
# GET    /student/{id}      → Retrieve one student           ✓ IMPLEMENTED
# POST   /student           → Create a new student           ✓ IMPLEMENTED
# PUT    /student/{id}      → Update an existing student     ✓ IMPLEMENTED
# DELETE /student/{id}      → Delete a student               ✗ NOT IMPLEMENTED
#
# ═════════════════════════════════════════════════════════════════════════════