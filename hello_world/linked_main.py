from fastapi import FastAPI,HTTPException

app=FastAPI()

student_db = {}

@app.post("/student")
def insert_student(student: dict[str, str]):
    if student.get("roll_number", None):
        student_db[student.get("roll_number")] = student
        return "Record Created!"
    else:
        return "Invalid Roll Number!"
    
@app.get("/student")
def get_student():
    return student_db

@app.get("/student/{roll_number}")
def get_student_by_roll_number(roll_number:str):
    try: 
        return student_db[roll_number]
    except Exception as e:
        raise HTTPException(status_code=200, detail="Invalid Roll Number!")
    
@app.put("/student/{roll_number}")
def update_student(roll_number, std: dict[str,str]):
    student_db[roll_number]=std
    return "Student Updated!"

@app.delete("/student/{roll_number}")
def delete_student(roll_number):
    student_db.pop(roll_number)
    return "Student Deleted!"

# http://localhost:8000/student
# http://localhost:8000/student/create
# http://localhost:8000/student/update
# http://localhost:8000/student/delete