from sqlmodel import Session, select
from model.student_model import Students

def get_student(session:Session, student_id:int):
    student = session.get(Students, student_id)
    return student

def get_student_list(session:Session):
    result = session.exec(select(Students)).all()
    return result

def insert_student_for_put(session:Session , student:Students):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def update_put_commit(session:Session, db_student:Students):
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student

def delete_student(student: Students , session: Session):
    session.delete(student)
    session.commit()