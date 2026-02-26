from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI, HTTPException

app = FastAPI()

class StudentOut(BaseModel):
    roll_number: str
    name:str
    email: EmailStr | None = None

class Student(BaseModel):
    roll_number: str
    name: str =Field(min_length=1, max_length=10)
    email:EmailStr
    password:str

    model_config = {
        "json_schema_extra": {"examples":[{
            "roll_number": "1",
            "name": "Ali",
            "email": "ali@gmail.com",
            "password":"123",
        }]}
    }
student_db = {}

@app.post("/student")
def insert_student(student:Student)->str:
    student_db[student.roll_number] =student
    return "Record Created!"

@app.get("/student")
def get_student():
    return student_db

@app.get("/student/{roll_number}", response_model=StudentOut)
def get_student_by_roll_number(roll_number:str) -> StudentOut:
    try:
        return student_db[roll_number]
    except Exception as ex:
        raise HTTPException(status_code=200, detail="Invalid Roll Number!")
    
@app.put("/student/{roll_number}")
def update_student(roll_number, std:Student):
    student_db[roll_number] = std
    return "Student Updated!"

@app.delete("/student/{roll_number}")
def delete_student(roll_number):
    student_db.pop(roll_number)
    return "Student Deleted!"

# http://localhost:8000/student
# http://localhost:8000/student/create
# http://localhost:8000/student/update
# http://localhost:8000/student/delete