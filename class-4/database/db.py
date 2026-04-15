from dotenv import load_dotenv
from sqlmodel import  create_engine, Session
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")
database_client = create_engine(str(database_url), echo=True) # echo=True - Logs all SQL queries to the console

def get_session():
    with Session(database_client) as session:
        yield session
