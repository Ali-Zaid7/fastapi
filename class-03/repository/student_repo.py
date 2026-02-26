from sqlmodel import Session
from model.student_model import Students

def get_student(session, student_id):
    return session.get(Students, student_id)

def update_put_commit(session:Session, db_student:Students):
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student

def insert_student_for_put(session:Session , student:Students):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student