from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import ZODB, ZODB.FileStorage
from pydantic import BaseModel

class ScoreUpdate(BaseModel):
    score: int

from class_module import *

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root
students = root.students

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    html_document = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        *{
            font-family: sans-serif;
            padding: 0;
            margin: 0;
        }
        .title{
            text-align: center;
            font-size: 30px;
            font-weight: bold;
        }
        form{
            width: 300px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        input{
            width: 100%;
            height: 30px;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="title">
        Login
    </div>
    <form method="post" action="/login">
        <div class="input">
            <label for="ID">ID:</label>
            <br>
            <input type="text" name="ID" id="ID" placeholder="ID">
        </div>
        <div class="input">
            <label for="password">Password:</label>
            <br>
            <input type="password" name="password" id="password" placeholder="Password">
        </div>
        <div class="input">
            <input type="submit" value="Login">
        </div>
    </form>
</body>
</html>
"""
    return html_document


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
async def student(ID: int):
    student = students[int(ID)]
    html_document = """
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        *{
            font-family: sans-serif;
            padding: 0;
            margin: 0;
        }
        .title{
            text-align: center;
            font-size: 30px;
            font-weight: bold;
        }
        .form-ctn{
            width: 600px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
            padding: 10px;
            margin-top: 20px;
        }
        input{
            width: 100%;
            height: 30px;
        }
        table{
            border-collapse: collapse;
            width: 100%;
        }
        table td, table th{
            text-align: center;
            padding: 10px;
            border: 1px solid black;
        }
        table th{
            background-color: #ededed;
        }
        input[type="submit"]{
            width: 100px;
            height: 30px;
            background-color: #329cff;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 0 auto;
            margin-top: 20px;
        }
        .name-holder{
            display: flex;
            justify-content: space-between;
            background-color: #ededed;
            padding: 10px;
        }
        .name-holder p{
            min-width: 100px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="title">
        Transcript Entry Form
    </div>
    <div class="form-ctn">
        <div class="name-holder">
        """
    html_document += f"""
            <p>ID: {student.id}</p>
            <p>Name: {student.name}</p>
        </div>
        <form action="">
            <table>
                <thead>
                    <tr>
                        <th>Course Code</th>
                        <th>Course Name</th>
                        <th>Credits</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
                """
    for enroll in student.enrolls:
        html_document += f"""
                    <tr>
                        <td>{enroll.course.id}</td>
                        <td>{enroll.course.name}</td>
                        <td>{enroll.course.credit}</td>
                        <td><input type="number" name="{enroll.course.id}" value="{enroll.score}"></td>
                    </tr>
                """   
    html_document += """
                </tbody>
            </table>
            <input type="submit" value="Submit">
        </form>
    </div>
</body>
"""
    html_document += """
<script>
const form = document.querySelector("form");
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const inputs = document.querySelectorAll("input[type='number']");
        const data_sand = {};
        inputs.forEach((input) => {
            data_sand[input.name] = input.value;
        });
        console.log(data_sand)
        fetch("/entry/1101",{
            method : "POST",
            headers : {
                "Content-Type" : "application/json"
            },
            body : JSON.stringify(data_sand),
        }).then((res) => {
            window.location.href = res.url;
        })
    });
</script>
</html>
"""
    return html_document

@app.post("/entry/{ID}")
async def entry(ID: int, data: dict):
    student = students[int(ID)]
    print(data)
    for enroll in student.enrolls:
        enroll.setScore(float(data[str(enroll.course.id)]))
        
    root.students[int(ID)] = student
    transaction.commit()
    return RedirectResponse(url=f"/transcript/{ID}", status_code=303)

@app.get("/transcript/{ID}", response_class=HTMLResponse)
async def transcript(ID: int):
    student = students[int(ID)]
    html_document = """
    
<!DOCTYPE html>
<html>
<head>
    <title>Unofficial Transcript</title>
    <style>
        body, html {
            height: 100%;
            text-align: center;
            justify-content: center;
            margin: auto;
            max-width: 900px;
        }
        table {
            text-align: center;
            justify-content: center;
        }
        th {
            border: 1px solid black;
            padding: 8px;
        }
        
        img {
            width: 100%; 
            height: auto; 
            display: block;
            margin: 0 auto; 
        }
        .center_top_col{
            width: 50%; 
            text-align: center;
        }
        .left_top_col {
            width: 35%; 
            text-align: left;
        }
        .mid_top_col {
            width: 15%; 
            text-align: left;
        }
        .right_top_col {
            text-align: left;
        }

        .content_table {
            border-collapse: collapse;
            width: 100%;
        }
        .content_table td {
            border: 1px solid black;
            padding: 8px;
            border-bottom: none;
            border-top: none;
        }
        .content_table tbody {
            border-bottom: 1px solid black;
        }
    </style>
</head>
<body>
    <br><br>
    <h1>( Unofficial Transcript )</h1>
    <table>
        <tbody>
            <tr>
                <td></td><td></td>
                <td rowspan="3" class="right_top_pic">
                    <img src="man.png" alt="transcript pic">
                </td>
            </tr>
            <tr>
                <td></td>
                <td class="center_top_col">
                    <h2>School of Engineering</h2>
                </td>
            </tr>
            <tr>
                <td class="left_top_col">
                    
                </td>
            </tr>
        </tbody>
    </table>
    <table>
        <tbody>
            <tr>
                <td class="left_top_col">
                """
    html_document += f"""
                    <label for="ID" style="font-style: italic;">ID</label>
                    <input type="text" id="ID" readonly value={student.id}>
                    <label for="name" style="font-style: italic;">Student Name</label>
                    <input type="text" id="name" value="{student.name}" readonly>
                    """
    html_document += f"""
                </td>
            </tr>
        </tbody>
    </table>
    <br>
    <table class="content_table">
        <thead>
            <th style="width: 85%;">
                <p>COURSE TITLE</p>
            </th>
            <th style="width: 5%;">
                <p>CREDIT</p>
            </th>
            <th style="width: 5%;">
                <p>SCORE</p>
            </th>
            <th style="width: 5%;">
                <p>GRADE</p>
            </th>
        </thead>
        <tbody id="content_body">
        """
    for enroll in student.enrolls:
        html_document += f"""
            <tr>
                <td style="text-align: left;">{enroll.course.name}</td>
                <td>{enroll.course.credit}</td>
                <td>{enroll.score}</td>
                <td>{enroll.getGrade()}</td>
            </tr>
        """
    html_document += f"""
            
        </tbody>
    </table>
    <br>
</body>
</html>
"""
    return html_document
@app.on_event("shutdown")
def shutdown_event():
    db.close()