from fastapi import FastAPI

app = FastAPI()

@app.get("/person")
def hello_world():
    return {"message": "Hello World"}

@app.get("/class")
def hello_class():
    return {"message": "hello class"}


@app.get("/person/{person_name}")
def hello_person(person_name):
    return {"message": "Hello Person :" + person_name}