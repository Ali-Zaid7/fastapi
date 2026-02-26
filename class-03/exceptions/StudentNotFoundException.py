from dataclasses import dataclass
from fastapi import HTTPException

@dataclass
class StudentNotFoundException(HTTPException):
    def __init__(self , status_code, detail):
        self.status_code = status_code
        self.detail = detail
