from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlmodel import SQLModel, select
from main import Students
from routes.student_route import router
from routes.student_route import router as student_router
from routes.course_route import router as course_router
from fastapi.responses import JSONResponse
from database.db import database_client, get_session

app = FastAPI()
app.include_router(student_router)
app.include_router(course_router)

# @app.middleware('http')
# async def test_middleware(request: Request, call_next) -> Response:
#     api_key = request.headers.get('X-API-KEY')
#     if api_key is None:
#         return JSONResponse(status_code=401, content={'detail': "API Key is Missing!"})
#     if api_key != '123':
#         return JSONResponse(status_code=401, content={'detail': "API Key is Invlaid!"})
    
#     response:Response = await call_next(request) # Send request to an endpoint which requested
#     response.headers['app_informartion'] = "Student Header"
#     return response
 
@app.get("/health")
def get_health():
    return "Server is Running..."

def create_table():
    SQLModel.metadata.create_all(database_client)
create_table()






# def get_config():
#     print("Config Function")
#     return {"app_name": "Student System", "version":1}

# def get_session():
#     with Session(database_client) as session:
#         yield session
