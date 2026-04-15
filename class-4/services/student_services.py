from fastapi import  status
from sqlmodel import Session
from exceptions.StudentNotFoundException import StudentNotFoundException
from model.student_model import Students
from sqlalchemy.exc import IntegrityError
from repository.student_repo import get_student, insert_student_for_put, update_put_commit, get_student_list

#session:Session=Depends(get_session) is wrong because Dependencies injection
#  is for framework called endpoint ,not by itself

# ⚠ WARNING: Parameter order must match the caller in app.py → put_update_student(session, student_id, student)
# A previous bug had (session, student, student_id) which caused session.get() to receive a Students object
# instead of an int, resulting in: "need the number of values in identifier to formulate primary key"

def get_student(session:Session):
    result = get_student_list(session)
    return result

def put_update_student(session:Session , student_id:int, student:Students):
    try: 
        db_student = get_student(session , student_id)
        if not db_student:
            raise StudentNotFoundException(status_code=status.HTTP_404_NOT_FOUND, detail="Roll Number or Email is Duplicate!")
                            
        data_student = student.model_dump(exclude_unset=True)

        for key, value in data_student.items():
            setattr(db_student, key, value)

        db_student= update_put_commit(session , db_student)
        return db_student

    except IntegrityError as ex:
        raise StudentNotFoundException(status_code=status.HTTP_409_CONFLICT, detail="Roll Number or Email is Duplicate!")
    
# For POST route
def create_student(session: Session, student:Students):
    try:
        student = insert_student_for_put(session , student)
        return student

    except IntegrityError as ex:
        return {"detail":"Roll number or Email is duplicate"}
