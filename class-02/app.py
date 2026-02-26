"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        FASTAPI STUDENT MANAGEMENT SYSTEM                      ║
║                      A Complete Learning Guide with Explanations              ║
╚═══════════════════════════════════════════════════════════════════════════════╝

📚 WHAT IS FASTAPI?
───────────────────
FastAPI is a modern Python web framework that helps you build APIs 
(Application Programming Interfaces). It's built on top of:
  - Starlette (for web handling and HTTP)
  - Pydantic (for data validation)
  
One of the FASTEST Python web frameworks available (hence the name!).

🤔 WHAT IS AN API?
──────────────────
API = Application Programming Interface

Think of your API as a "menu" in a restaurant:
  ✓ Clients (web browsers, mobile apps, other programs) place REQUESTS
  ✓ Your server PROCESSES the request (query database, run logic)
  ✓ Your server sends back a RESPONSE (usually JSON data)

INSTEAD OF manually entering a database, clients request data via HTTP URLs:
  GET    /student         → Get all students
  GET    /student/1       → Get student with ID=1
  POST   /student         → Create a new student  
  PUT    /student/1       → Update student with ID=1
  DELETE /student/1       → Delete student with ID=1

✨ WHY USE FASTAPI?
───────────────────
✓ SPEED - One of the fastest Python web frameworks (faster than Flask, Django)
✓ INTUITIVE - Easy and beautiful code to write
✓ AUTOMATIC API DOCS - Generates interactive Swagger UI documentation automatically
✓ DATA VALIDATION - Validates all incoming data automatically (no manual checks!)
✓ TYPE HINTS - Uses Python 3.6+ type hints for better code quality
✓ ERROR HANDLING - Automatic error messages if data is invalid

🎯 WHAT IS THIS app.py DOING?
──────────────────────────────
This is a STUDENT MANAGEMENT SYSTEM API.

MOTIVE: Build a system where:
  ✓ We can VIEW all students
  ✓ We can VIEW a specific student by ID
  ✓ We can ADD (CREATE) new students
  ✓ We can MODIFY (UPDATE) existing students
  ✓ Data is stored in a PostgreSQL database

CRUD Operations Summary:
  C = CREATE (add new students with POST)
  R = READ   (get students with GET)
  U = UPDATE (modify students with PUT)
  D = DELETE (remove students - not implemented here)

The system uses PostgreSQL (a professional database) hosted on Neon Cloud.

═══════════════════════════════════════════════════════════════════════════════
"""

# IMPORTS: Bringing in external libraries to use in our code
# ─────────────────────────────────────────────────────────────

# FastAPI = The main framework for building web APIs
# Depends = A function that allows dependency injection (injects dependencies automatically)
# HTTPException = A way to send error responses (like 404 "Not Found", 500 "Server Error")
from fastapi import FastAPI, Depends, HTTPException

# SQLModel = A library that combines SQLAlchemy (database ORM) with Pydantic (validation)
# create_engine = Creates and configures a database connection
# Session = Manages database transactions (opening/closing connections, saving changes)
# SQLModel = Base class for creating database models (blueprints for database tables)
# select = Used to query data from the database (like writing SQL SELECT statements)
# Field = Used to define column properties (defaults, constraints, primary keys, etc.)
from sqlmodel import create_engine, Session, SQLModel, select, Field

# IntegrityError = An exception (error) that occurs when database constraints are violated
# Example: Trying to insert two students with the same email (violates unique constraint)
from sqlalchemy.exc import IntegrityError

# ═════════════════════════════════════════════════════════════════════════════

# STEP 1: CREATE THE FASTAPI APPLICATION INSTANCE
# ────────────────────────────────────────────────
# This creates the main FastAPI "app" object. Think of it as the CORE/HEART of your API.
# All HTTP routes (endpoints) will be registered to this app object.
app = FastAPI()

# ═════════════════════════════════════════════════════════════════════════════

# STEP 2: SET UP THE DATABASE CONNECTION STRING
# ──────────────────────────────────────────────

# database_url: This is the CONNECTION STRING that tells Python WHERE and HOW to connect to the database
#
# Breaking down the URL:
#   postgresql://          = We're using PostgreSQL (popular SQL database system)
#   neondb_owner           = Username to log into the database
#   :npg_Epj6LHRg...      = Password for authentication (secret key)
#   @ep-plain-breeze...    = The server address (host) where database is located (cloud server)
#   giaic_student          = The database NAME (like a folder of tables)
#   ?sslmode=require       = Use encrypted SSL connection for security
database_url = "postgresql://neondb_owner:npg_Epj6LHRgFaY0@ep-plain-breeze-a178ieg2-pooler.ap-southeast-1.aws.neon.tech/giaic_student?sslmode=require"

# create_engine(): Creates a database connection pool
# echo=True: Print all SQL queries to console (useful for debugging - see what queries are running)
database_client = create_engine(database_url, echo=True)


class Students(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    roll_number: int
    phone_number: str


# def create_table():
#     SQLModel.metadata.create_all(database_client)

# create_table()


def get_config():
    print("config function")
    return {"app_name": "student system", "version": 1}


def get_session():
    with Session(database_client) as session:
        yield session




# ═════════════════════════════════════════════════════════════════════════════
# STEP 7: ROUTE 1 - GET ALL STUDENTS
# ═════════════════════════════════════════════════════════════════════════════

# @app.get("/student")
# This is a "ROUTE DECORATOR" (the @ symbol)
# It tells FastAPI: "When someone makes a GET request to /student, run this function"
#
# GET = A request method for RETRIEVING data (read-only, doesn't change anything)
# "/student" = The URL path (endpoint) for this route
# 
# HTTP Request Example:
#   GET http://localhost:8000/student
# 
# Expected Response:
#   200 OK with list of all students in JSON format

@app.get("/student")
def get_student_list(session=Depends(get_session)):
    """
    GET /student endpoint: Retrieve all students from the database
    
    Parameters:
    -----------
    session=Depends(get_session):
      - 'session' is the database session/connection
      - 'Depends(get_session)' tells FastAPI to automatically call get_session() and pass result here
      - This is DEPENDENCY INJECTION in action!
    
    Returns:
    --------
    A list of all Student objects from the database (as JSON)
    """
    
    # session.exec() = Execute a database query
    # select(Students) = SQL equivalent: SELECT * FROM students
    #     This creates a query object that says "give me all Students"
    # .all() = Fetch ALL results from the query (returns a list)
    result = session.exec(select(Students)).all()
    
    return result  # FastAPI automatically converts this to JSON


# ═════════════════════════════════════════════════════════════════════════════
# STEP 8: ROUTE 2 - GET A SPECIFIC STUDENT BY ID
# ═════════════════════════════════════════════════════════════════════════════

# @app.get("/student/{student_id}")
# The curly braces {student_id} create a PATH PARAMETER
# 
# HTTP Request Examples:
#   GET /student/1      ← Returns student with ID=1
#   GET /student/42     ← Returns student with ID=42
#
# The number at the end is captured as the student_id variable

@app.get("/student/{student_id}")
def get_student(student_id: int, session=Depends(get_session)):
    """
    GET /student/{student_id} endpoint: Retrieve a specific student by their ID
    
    Parameters:
    -----------
    student_id: int
      - The student's unique ID (from the URL path)
      - ': int' means this MUST be an integer
      - FastAPI automatically validates and converts it to int
    
    session=Depends(get_session)
      - Database session (automatically provided)
    
    Returns:
    --------
    A single Student object (as JSON), or a 404 error if not found
    """
    
    # session.get(Students, student_id)
    # This is like doing: SELECT * FROM students WHERE id = {student_id}
    # It queries the database for a Student with the matching ID
    result = session.get(Students, student_id)
    
    # Check if the student was found
    if not result:
        # If student not found, return a 404 (Not Found) HTTP error
        # status_code=404 = "Resource not found" HTTP status
        # detail = The error message to send to the client
        raise HTTPException(status_code=404, detail="student not found")
    
    return result  # Return the found student


# ═════════════════════════════════════════════════════════════════════════════
# STEP 9: ROUTE 3 - CREATE A NEW STUDENT (POST)
# ═════════════════════════════════════════════════════════════════════════════

# @app.post("/student")
# POST = A request method for CREATING new data
# 
# HTTP Request Example:
#   POST /student
#   Content-Type: application/json
#   {
#     "name": "Ahmed",
#     "email": "ahmed@example.com",
#     "roll_number": 101,
#     "phone_number": "+923001234567"
#   }
#
# Expected Response:
#   201 Created (or 200 OK) with the newly created student object

@app.post("/student")
def post_student(student: Students, session=Depends(get_session)):
    """
    POST /student endpoint: Create a new student
    
    Parameters:
    -----------
    student: Students
      - This expects a JSON body matching our Students model
      - FastAPI automatically validates the JSON against the Students schema
      - If validation fails, it returns a 422 error automatically
    
    session=Depends(get_session)
      - Database session for saving the student
    
    Returns:
    --------
    The newly created Student object (as JSON), or error if duplicate email/roll_number
    """
    
    try:
        # session.add(student)
        # This tells the database: "I want to INSERT this student"
        # Note: It doesn't actually save yet, it's just staged for saving
        session.add(student)
        
        # session.commit()
        # This ACTUALLY SAVES the student to the database
        # Like pressing "Save" in a text editor
        session.commit()
        
        # session.refresh(student)
        # Re-fetch the student from database to get the auto-generated ID
        # (The database automatically assigns the ID when we save)
        session.refresh(student)
        
        return student  # Return the created student with its new ID
        
    # IntegrityError occurs when we violate database constraints
    # (like trying to insert duplicate email or roll_number)
    except IntegrityError as ex:
        return {"detail": "roll number or email is duplicate"}




# ═════════════════════════════════════════════════════════════════════════════
# STEP 10: ROUTE 4 - UPDATE A STUDENT (PUT)
# ═════════════════════════════════════════════════════════════════════════════

# @app.put("/student/{student_id}")
# PUT = A request method for UPDATING existing data
# 
# HTTP Request Example:
#   PUT /student/1
#   Content-Type: application/json
#   {
#     "name": "New Name"
#     "email": "new@example.com"
#   }
#
# This updates the student with ID=1 with the new information
# Note: You don't need to send all fields, only the ones you want to change

@app.put("/student/{student_id}")
def put_student(student_id: int, student: Students, session=Depends(get_session)):
    """
    PUT /student/{student_id} endpoint: Update an existing student
    
    Parameters:
    -----------
    student_id: int
      - The ID of the student to update
    
    student: Students
      - The updated student data (as JSON body)
      - You can send partial data (not all fields required)
    
    session=Depends(get_session)
      - Database session for fetching and saving
    
    Returns:
    --------
    The updated Student object (as JSON), or 404 if not found
    """
    
    try:
        
        # First, find the existing student in the database
        # session.get(Students, student_id)
        # This is like: SELECT * FROM students WHERE id = {student_id}
        db_student = session.get(Students, student_id)
        
        # Check if student exists
        if not db_student:
            raise HTTPException(status_code=404, detail="student not found")
        
        # Convert the incoming student data to a dictionary
        # .model_dump() = Convert the Pydantic model to a Python dictionary
        # exclude_unset=True = Only include fields that the user actually sent
        #   This is important! If a field isn't sent by the user, we don't want to overwrite it with None
        #
        # Example:
        #   If user sends: {"name": "New Name"}
        #   model_dump(exclude_unset=True) returns: {"name": "New Name"}  (NOT {"name": "New Name", "email": None, ...})
        data_student = student.model_dump(exclude_unset=True)
        
        # Loop through each field that the user wants to update
        # for key, value in data_student.items():
        #   key = field name (like "name", "email", "phone_number")
        #   value = the new value for that field
        for key, value in data_student.items():
            # setattr(object, attribute_name, value)
            # This dynamically sets an attribute on an object
            # It's like doing: db_student.name = value (but works for any field)
            setattr(db_student, key, value)
        
        # Below are ALTERNATIVE approaches (commented out) that do the same thing manually:
        # Instead of looping, you could explicitly update each field:
        # if student.name:
        #     db_student.name = student.name
        # if student.email:
        #     db_student.email = student.email
        # if student.phone_number:
        #     db_student.phone_number = student.phone_number
        # if student.roll_number:
        #     db_student.roll_number = student.roll_number
        
        # The loop approach (using setattr) is more flexible and requires less code!
        
        # Now save the updated student back to the database
        session.add(db_student)      # Stage the update
        session.commit()              # Actually save to database
        session.refresh(db_student)   # Re-fetch to confirm the changes
        
        return db_student  # Return the updated student

        
    # Handle constraint violations (duplicate email or roll_number)
    except IntegrityError as ex:
        return {"detail": "roll number or email is duplicate"}


# ═════════════════════════════════════════════════════════════════════════════
# HOW TO RUN THIS APPLICATION:
# ═════════════════════════════════════════════════════════════════════════════
#
# In your terminal, run:
#   uvicorn app:app --reload
#
# What this means:
#   uvicorn = Server that runs FastAPI applications
#   app:app = Tell uvicorn where the FastAPI instance is (module:variable)
#   --reload = Auto-reload when code changes (useful during development)
#
# Then open your browser and go to:
#   http://localhost:8000/docs  ← Interactive API documentation (Swagger UI)
#   http://localhost:8000/redoc ← Alternative documentation (ReDoc)
#
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