from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Dict
import ZODB, ZODB.FileStorage
from pydantic import BaseModel
from class_module import *

class ScoreUpdate(BaseModel):
    id: int
    score: float
    
templates = Jinja2Templates(directory="templates")
storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root
students = root.students

app = FastAPI()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post('/login')
async def login(ID: int = Form(...), password: str = Form(...) ):
    if int(ID) in students.keys():
        print(ID, password, students[int(ID)].id, students[int(ID)].password)
        if(students[int(ID)].login(ID, password)):
            
            # return response with get method
            return RedirectResponse(url=f"/student/{ID}", status_code=303)
        else:
            return {"message": "Wrong password"}
    else:
        return {"message": "ID not found"}

@app.get("/redirect/{ID}")
def redirect(ID: int):
    return RedirectResponse(url=f"/student/{ID}")

@app.get("/student/{ID}", response_class=HTMLResponse)
async def student(ID: int, request: Request):
    student = students[int(ID)]
    data = {
        "title": "Example Template",
        "message": "This is an example template with FastAPI and Jinja2",
        "student": student,
        "ID": ID
    }
    return templates.TemplateResponse("userform.html", {"request": request, "data": data})

@app.post("/entry/{ID}")
async def entry(ID: int, request: Request):
    
    student = students.get(ID)
    
    scores = await request.form()
    for key in scores.keys():
        for enroll in student.enrolls:
            if int(enroll.course.id) == int(key):
                enroll.score = float(scores[key])
        
    root.students[int(ID)] = student
    transaction.commit()
    return RedirectResponse(url=f"/transcript/{ID}", status_code=303)

@app.get("/transcript/{ID}")
async def transcript(ID: int, request: Request):
    student = students[int(ID)]
    data = {
        "student": student,
        "ID": ID
    }
    return templates.TemplateResponse("transcript.html", {"request": request, "data": data})
@app.on_event("shutdown")
def shutdown_event():
    db.close()