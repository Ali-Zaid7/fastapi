from sqlmodel import SQLModel
from database.db import database_client
from model.student_model import Students
from model.course_model import Course

print("Creating tables...")
SQLModel.metadata.create_all(database_client)
print("Tables created successfully!")
