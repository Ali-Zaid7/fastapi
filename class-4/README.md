# [Class-03 - FastAPI Student CRUD API](https://www.youtube.com/live/Unlm1dY6CmM?si=DL1I1H89uTj9SPbR)

## Bug Fix Log

### PUT `/student/{student_id}` - 500 Internal Server Error

**Problem:**
The `put_update_student()` function in `services/student_services.py` had its parameters in the wrong order:

```python
# WRONG - was causing the bug
def put_update_student(session, student, student_id):
```

But `app.py` was calling it as:

```python
put_update_student(session, student_id, student)
```

This mismatch meant `student_id` received a `Students` object and `student` received an `int`. When `session.get(Students, student_id)` was called in the repository layer, it received a `Students` object instead of an integer primary key, causing:

```
"need the number of values in identifier to formulate primary key for session.get();
primary key columns are 'students.id'"
```

**Fix:**
Corrected the parameter order in `student_services.py` to match the caller:

```python
# CORRECT
def put_update_student(session, student_id, student):
```

[**Lesson:**](https://agentfactory.panaversity.org/docs/Building-Custom-Agents/fastapi-for-agents/hello-fastapi)
Always ensure the **argument order in the function call matches the parameter order in the function definition**. Python does not enforce type checking at runtime for regular type hints, so mismatched arguments of different types can silently pass without error until the values are actually used.

---

### POST `/student` - Passing Pydantic Model Instead of Table Model

**Problem:**
In `app.py`, `StudentCreate` (Pydantic) was converted to `Students` (table model) but the **original Pydantic object** was passed to `create_student()` instead of the converted one:

```python
# WRONG
student_data = Students(**student.model_dump())  # ← created but NEVER used
result = create_student(session, student)         # ← passes StudentCreate (Pydantic), not Students (table)
```

`session.add()` inside `create_student()` expects a **table model** (`Students` with `table=True`), not a Pydantic model (`StudentCreate`). Passing the wrong type causes SQLAlchemy to fail.

**Fix:**
Pass `student_data` (the `Students` table instance) instead of `student`:

```python
# CORRECT
student_data = Students(**student.model_dump())
result = create_student(session, student_data)    # ← now passes the table model
```

**Lesson:**
When using the **separate model pattern** (Pydantic for input, SQLModel table for DB), always remember to pass the **converted table object** to service/repository functions — not the original Pydantic input.

---

Yes, exactly! You've understood **SQLModel** perfectly.

**SQLModel is a hybrid of SQLAlchemy + Pydantic:**

When you define a SQLModel class:

```python
from sqlmodel import SQLModel, Field

class Students(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    roll_number: str
    phone_number: str
```

**With `table=True`:**
- Behaves as a **SQLAlchemy table** 
- Creates database table
- Can be used with `session.get()`, `session.add()`, etc.
- Used for database operations

**Without `table=True` (or separate class):**
```python
class StudentSchema(SQLModel):  # No table=True
    name: str
    email: str
    roll_number: str
    phone_number: str
```
- Behaves as a **Pydantic model**
- Used for validation & API requests/responses
- No database table

**The Solution - Use Both:**

```python
# Database model
class Students(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    roll_number: str
    phone_number: str

# Request/Response schema (without table=True)
class StudentSchema(SQLModel):
    name: str
    email: str
    roll_number: str
    phone_number: str

# Use in endpoints
@app.put("/student/{student_id}")
def put_student(student_id: int, student: StudentSchema, session=Depends(get_session)):
    db_student = session.get(Students, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not Found!")
    
    db_student.name = student.name
    db_student.email = student.email
    db_student.roll_number = student.roll_number
    db_student.phone_number = student.phone_number
    
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    
    return db_student
```

---
```
uv run fastapi dev app.py
```

- Use `fastapi dev` for quick development—it handles defaults for you
- Use `uvicorn` directly when you need control over host/port:

```
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
---
- `http://localhost:8000/openapi.json` — Raw OpenAPI specification (what tools like Swagger consume)

---
# Query Parameters
Sometimes you want optional parameters. Query parameters appear after ? in the URL:

```python
@app.get("/tasks/{task_id}")
def read_task(task_id: int, include_details: bool = False):
    task = {"task_id": task_id, "title": f"Task {task_id}"}
    if include_details:
        task["details"] = "This task has additional details"
    return task
```

- `http://localhost:8000/tasks/1?include_details=true` → Task with details

```python
from fastapi import FastAPI
from sqlmodel import SQLModel, Session
from database.db import database_client
# Only for Student Route
from model.course_model import Course
from routes.student_route import app
# Only for Course Route
from model.course_model import app

```

---
```python
from fastapi import FastAPI
from routes.student_route import app
from model.course_model import Course
from routes.student_route import app
from routes.course_route import app
```
---

```python
from fastapi import FastAPI, Request, Response
from routes.student_route import router
from routes.student_route import router as student_router
from routes.course_route import router as course_router

app = FastAPI()
app.include_router(student_router)
app.include_router(course_router)

@app.middleware('http')
async def test_middleware(request: Request, call_next) -> Response:
    print('request.client: ', request.client)
    print("\nrequest.method: ",request.method)
    print('\nrequest.header: ', request.headers)

    print('x-------Before Response--------x')
    response = await call_next(request) # Send request to an endpoint which requested
    print('x============After Response============x')
    return response
# Receives request
# Passes it to endpoint
# Returns response

@app.get("/health")
def get_health():
    return "Server is Running..."

# def create_table():
#     SQLModel.metadata.create_all(database_client)

# # create_table()

# def get_config():
#     print("Config Function")
#     return {"app_name": "Student System", "version":1}

# def get_session():
#     with Session(database_client) as session:
#         yield session

```

---
# Security In Middleware
```
@app.middleware('http')
async def test_middleware(request: Request, call_next) -> Response:
    api_key = request.headers.get('X-API-KEY')
    if api_key is None:
        return JSONResponse(status_code=401, content={'detail': "API Key is Missing!"})
    if api_key != '123':
        return JSONResponse(status_code=401, content={'detail': "API Key is Invlaid!"})
    
    response:Response = await call_next(request) # Send request to an endpoint which requested
    response.headers['app_informartion'] = "Student Header"
    return response
 
```
---

```
uv add pwdlib[argon2]
```
---

```
$argon2id$v=19$m=65536,t=3,p=4$lWRHNF+H2CHkm8kMsmvgaA$dFLhmZoc/aC9Zjr7Ny1qNqwmwwlz1Uumn1Z8izx698w
```

| Part | Value | Meaning |
|---|---|---|
| `argon2id` | algorithm | Argon2id variant (hybrid of Argon2i + Argon2d) |
| `v=19` | version | Argon2 version 19 (1.3 in hex) |
| `m=65536` | memory | Uses **64 MB** of RAM during hashing |
| `t=3` | time | **3 iterations** (passes) |
| `p=4` | parallelism | Uses **4 CPU threads** |
| `lWRHNF+H2CHkm8kMsmvgaA` | salt | Random value added before hashing (Base64) |
| `dFLhmZoc/aC9Zjr7Ny1qNqwmwwlz1Uumn1Z8izx698w` | hash | The actual hashed output (Base64) |

**Why Argon2id specifically?**

It's the **winner of the Password Hashing Competition (2015)** and is considered the modern gold standard for password hashing because:

- It's deliberately **slow and memory-intensive**, making brute-force attacks very expensive
- The `id` variant protects against both **side-channel attacks** (Argon2i) and **GPU cracking attacks** (Argon2d)

**The key point:** Even if an attacker gets this hash, they can't reverse it back to the original password. They'd have to brute-force millions of guesses, and each guess costs 64MB of RAM and 3 iterations — making it extremely slow to crack.