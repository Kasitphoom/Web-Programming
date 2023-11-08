from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
import ZODB, ZODB.FileStorage
import transaction

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root
students = root.students

template = Jinja2Templates(directory="templates")
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return template.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def set_login(request: Request, response: Response, ID: int = Form(...), password: str = Form(...)):
    if ID in students.keys():
        if students[ID].login(ID, password):
            response = RedirectResponse(url="/userform", status_code=303)
            response.set_cookie(key="ID", value=ID)
            return response
        else:
            return {"message": "Login failed"}
    else: 
        return {"message": "No student found"}

@app.get("/userform", response_class=HTMLResponse)
async def userform(request: Request, ID: int = Cookie(None)):
    print(ID)
    data = {
        "student": students[ID],
        "ID": ID,
    }
    if ID in students.keys():
        return template.TemplateResponse("userform.html", {"request": request, "data": data})
    else:
        return RedirectResponse(url="/", status_code=303)
    
@app.post("/entry")
async def entry(request: Request, ID: int = Cookie(None)):
    if ID == None:
        return {"message": "Missing Cookie"}
    student = students[ID]
    scores = await request.form()
    for key in scores.keys():
        for enrolled in student.enrolls:
            if enrolled.course.id == key:
                enrolled.score = float(scores[key])
                
    root.students[ID] = student
    transaction.commit()
    return RedirectResponse(url="/transcript", status_code=303)

@app.get("/transcript", response_class=HTMLResponse)
async def transcript(request: Request, ID: int = Cookie(None)):
    data = {
        "student": students[ID],
    }
    return template.TemplateResponse("transcript.html", {"request": request, "data": data})