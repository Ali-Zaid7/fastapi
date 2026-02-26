from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Field, SQLModel, create_engine, Session, SQLModel , select
from sqlalchemy.exc import IntegrityError


app = FastAPI()

database_url = database_url
database_client = create_engine(database_url, echo=True) # echo=True - Logs all SQL queries to the console

class Students(SQLModel, table=True):
    id: int | None = Field(default=None , primary_key=True)
    name: str
    email: str
    roll_number: int
    phone_number: str

def create_table():
    SQLModel.metadata.create_all(database_client)

# create_table()

def get_config():
    print("Config Function")
    return {"app_name": "Student System", "version":1}

def get_session():
    with Session(database_client) as session:
        yield session

@app.get("/student")
def get_student_list(session=Depends(get_session)):
    result = session.exec(select(Students)).all()
    return result

@app.get("/student/{student_id}")
def get_student(student_id:int , session=Depends(get_session)):
    result = session.get(Students, student_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student not Found!")
    return result

@app.post("/student")
def post_student(student: Students, session=Depends(get_session)):
    try:
        session.add(student)
        session.commit()
        session.refresh(student)
        return student
    
    except IntegrityError as ex:
        return {"detail":"Roll number or Email is duplicate"}
    
@app.put("/student/{student_id}")
def put_student(student_id:int, student:Students, session=Depends(get_session)):
    try:
        db_student = session.get(Students, student_id)
        if not db_student:
            raise HTTPException(status_code=404, detail="Student Not Found!")
        
        data_student = student.model_dump(exclude_unset=True)

        for key, value in data_student.items():
            setattr(db_student, key, value)

        session.add(db_student)
        session.commit()
        session.refresh(db_student)

        return db_student
    
    except IntegrityError as ex:
        return {"detail":"Roll Number or Email is Duplicate"}
    
@app.patch("/student/{student_id}")
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
        
        
@app.delete("/student/{student_id}")
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
