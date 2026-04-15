from model.course_model import Course
from fastapi import  Depends, APIRouter
from database.db import get_session

router = APIRouter()
courses = ['python' , 'nextjs', 'FastAPI']

@router.get("/course")
def get_courses_list(session=Depends(get_session)):
    return courses

@router.get("/course/{course_id}")
def get_courses(course_id: int,session=Depends(get_session)):
    try:
        return courses[course_id]
    except Exception as er:
        return f'The Course of id: {course_id} is not exist!'

@router.post("/course")
def post_course(course: Course,session=Depends(get_session)):
    return "Course Created!"

@router.put("/course/{course_id}")
def put_course(course_id:int ,course: Course,session=Depends(get_session)):
    return "Course Updated!"

@router.patch("/course/{course_id}")
def post_course(course_id:int ,course: Course,session=Depends(get_session)):
    return "Course Update with Particular property!"

@router.delete("/course/{course_id}")
def post_course(course_id:int,course: Course,session=Depends(get_session)):
    return "Course Deleted!"
