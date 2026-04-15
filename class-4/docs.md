# Database Setup Guide - FastAPI with SQLModel

This guide covers everything about creating databases and tables using SQLModel with PostgreSQL (Neon).

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Database Connection Setup](#database-connection-setup)
3. [Creating Table Models](#creating-table-models)
4. [Creating Tables in Database](#creating-tables-in-database)
5. [Common Errors & Solutions](#common-errors--solutions)
6. [Best Practices](#best-practices)

---

## Prerequisites

- Python 3.10+
- SQLModel installed (`pip install sqlmodel`)
- PostgreSQL database (e.g., Neon, local PostgreSQL)
- python-dotenv for environment variables (`pip install python-dotenv`)

---

## Database Connection Setup

### Step 1: Create `.env` File

Create a `.env` file in your project root:

```env
DATABASE_URL="postgresql://username:password@host:port/database_name?sslmode=require"
```

**Example (Neon):**
```env
DATABASE_URL="postgresql://neondb_owner:npg_xxx@ep-xxx.us-east-1.aws.neon.tech/fastapi_practice?sslmode=require"
```

### Step 2: Create Database Module (`database/db.py`)

```python
from dotenv import load_dotenv
from sqlmodel import create_engine, Session
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")
database_client = create_engine(str(database_url), echo=True)  # echo=True logs SQL queries

def get_session():
    with Session(database_client) as session:
        yield session
```

---

## Creating Table Models

### Basic Model Structure

Create models in `model/` directory:

```python
# model/student_model.py
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Integer, Identity, VARCHAR

class Students(SQLModel, table=True):
    id: int | None = Field(default=None, sa_column=Column(Integer, Identity(), primary_key=True))
    name: str = Field(sa_column=Column(VARCHAR(255), nullable=False))
    email: str = Field(sa_column=Column(VARCHAR(255), nullable=False, unique=True))
    roll_number: int = Field(sa_column=Column(VARCHAR(255), nullable=False))
    phone_number: str = Field(sa_column=Column(VARCHAR(15), nullable=True))
```

### Field Options Explained

| Parameter | Description | Example |
|-----------|-------------|---------|
| `default=None` | Default value for the field | `default=None` |
| `primary_key=True` | Marks field as primary key | `primary_key=True` |
| `sa_column` | Custom SQLAlchemy column configuration | `sa_column=Column(...)` |
| `nullable=False` | Column cannot be NULL | `nullable=False` |
| `unique=True` | Values must be unique | `unique=True` |

### SQLAlchemy Column Types

| Type | Usage |
|------|-------|
| `Integer` | Whole numbers |
| `VARCHAR(n)` | Variable-length string (max n characters) |
| `Text` | Long text |
| `Boolean` | True/False |
| `DateTime` | Date and time |
| `Float` | Decimal numbers |

### Identity (Auto-increment)

```python
# Auto-incrementing primary key
id: int | None = Field(default=None, sa_column=Column(Integer, Identity(), primary_key=True))
```

### Complete Model with All Classes

```python
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Integer, Identity, VARCHAR, Text

# Database Table Model
class Course(SQLModel, table=True):
    id: int | None = Field(default=None, sa_column=Column(Integer, Identity(), primary_key=True))
    course_name: str = Field(sa_column=Column(VARCHAR(255), nullable=False, unique=True))
    course_detail: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
    instructor: str | None = Field(default=None, sa_column=Column(VARCHAR(255), nullable=True))
    duration: int | None = Field(default=None, sa_column=Column(Integer, nullable=True))

# Request Models
class CourseCreate(SQLModel):
    course_name: str
    course_detail: str | None = None
    instructor: str | None = None
    duration: int | None = None

class CourseUpdate(SQLModel):
    course_name: str
    course_detail: str | None = None
    instructor: str | None = None
    duration: int | None = None

class CourseUpdateField(SQLModel):
    course_name: str | None = None
    course_detail: str | None = None
    instructor: str | None = None
    duration: int | None = None

# Response Models
class CourseRead(SQLModel):
    id: int
    course_name: str
    course_detail: str | None = None
    instructor: str | None = None
    duration: int | None = None
```

---

## Creating Tables in Database

### Method 1: Create Tables Script (Recommended for Development)

Create `create_tables.py`:

```python
from sqlmodel import SQLModel
from database.db import database_client

# Import ALL models to register them
from model.student_model import Students
from model.course_model import Course

print("Creating tables...")
SQLModel.metadata.create_all(database_client)
print("Tables created successfully!")
```

**Run the script:**
```bash
uv run python create_tables.py
```

### Method 2: Create Tables on App Startup (Development Only)

```python
# app.py
from fastapi import FastAPI
from sqlmodel import SQLModel
from database.db import database_client
from model.student_model import Students
from model.course_model import Course

app = FastAPI()

# Create tables on startup (remove in production)
SQLModel.metadata.create_all(database_client)

@app.get("/health")
def get_health():
    return "Server is Running..."
```

### Method 3: Using Alembic (Production Ready)

Alembic handles database migrations:

```bash
# Install alembic
pip install alembic

# Initialize alembic
alembic init alembic

# Configure alembic.ini with your DATABASE_URL

# Create a migration
alembic revision --autogenerate -m "Create students and courses tables"

# Apply migration
alembic upgrade head
```

---

## Common Errors & Solutions

### Error 1: No Primary Key

**Error:**
```
sqlalchemy.exc.ArgumentError: Mapper could not assemble any primary key columns
```

**Cause:** Missing `primary_key=True` in id field

**Solution:**
```python
# ❌ Wrong
id: int | None = Field(default=None, sa_column=Column(VARCHAR(255), nullable=False))

# ✅ Correct
id: int | None = Field(default=None, sa_column=Column(Integer, Identity(), primary_key=True))
```

---

### Error 2: Field() Takes Too Many Positional Arguments

**Error:**
```
TypeError: Field() takes from 0 to 1 positional arguments but 2 were given
```

**Cause:** Passing `Integer, Identity()` as positional arguments

**Solution:**
```python
# ❌ Wrong
id: int | None = Field(Integer, Identity(), primary_key=True)

# ✅ Correct
id: int | None = Field(default=None, sa_column=Column(Integer, Identity(), primary_key=True))
```

---

### Error 3: Table Not Created in Database

**Cause:** `create_all()` was never called

**Solution:** Run the `create_tables.py` script or call `SQLModel.metadata.create_all(database_client)`

---

### Error 4: Connection Error

**Error:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Cause:** Invalid DATABASE_URL or network issues

**Solution:**
- Check DATABASE_URL in `.env`
- Verify database credentials
- Check network/firewall settings

---

## Best Practices

### 1. Model Organization

```
project/
├── model/
│   ├── student_model.py
│   └── course_model.py
├── database/
│   └── db.py
├── routes/
├── services/
└── repository/
```

### 2. Separate Request/Response Models

```python
# Table model (database)
class Student(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str
    email: str

# Create request
class StudentCreate(SQLModel):
    name: str
    email: str

# Response model
class StudentRead(SQLModel):
    id: int
    name: str
    email: str
```

### 3. Use Environment Variables

Never hardcode database credentials:

```python
# ✅ Good
database_url = os.getenv("DATABASE_URL")

# ❌ Bad
database_url = "postgresql://user:password@host/db"
```

### 4. Add Indexes for Frequently Queried Columns

```python
from sqlalchemy import Index

class Students(SQLModel, table=True):
    __table_args__ = (
        Index('ix_students_email', 'email'),
        Index('ix_students_roll_number', 'roll_number'),
    )
    id: int | None = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
```

### 5. Use Migrations in Production

- Use **Alembic** for production databases
- Track schema changes
- Enable rollback capabilities

### 6. Echo Mode for Debugging

```python
# Enable SQL logging (development only)
database_client = create_engine(database_url, echo=True)

# Disable in production
database_client = create_engine(database_url, echo=False)
```

---

## Quick Reference

### Complete Table Creation Checklist

- [ ] Create `.env` with `DATABASE_URL`
- [ ] Setup `database/db.py` with engine and session
- [ ] Create model classes with `table=True`
- [ ] Define primary key with `Identity()`
- [ ] Import all models in `create_tables.py`
- [ ] Run `SQLModel.metadata.create_all(database_client)`
- [ ] Verify tables in database console

### Common Field Patterns

```python
# Auto-increment Primary Key
id: int | None = Field(default=None, sa_column=Column(Integer, Identity(), primary_key=True))

# Required String
name: str = Field(sa_column=Column(VARCHAR(255), nullable=False))

# Unique String
email: str = Field(sa_column=Column(VARCHAR(255), nullable=False, unique=True))

# Optional String
description: str | None = Field(default=None, sa_column=Column(Text, nullable=True))

# Optional Integer
age: int | None = Field(default=None, sa_column=Column(Integer, nullable=True))

# Boolean
is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
```

---

## Resources

- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Neon Database](https://neon.tech/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
