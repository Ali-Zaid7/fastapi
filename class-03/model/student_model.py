from sqlmodel import Field, SQLModel


class Students(SQLModel, table=True):
    id: int | None = Field(default=None , primary_key=True)
    name: str
    email: str
    roll_number: int
    phone_number: str

class StudentCreate(SQLModel):
    name: str
    email: str
    roll_number: int
    phone_number: str