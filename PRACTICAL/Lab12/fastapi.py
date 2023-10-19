from fastapi import FastAPI

students = {}

@app.get('/students/{id}')

async def root(id: str):
    
    if id == 'all':
        return students
    else:
        if id in students:
            return students[id]
        else:
            return {"error": "Student not found"}
        
# on body
@app.post('/students/new')

async def root(id: str, first_name: str, last_name: int):
    
    if id in students:
        return {"error": "Student already exists"}
    else:
        students[id] = {"ID": id, "first_name": first_name, "last_name": last_name}
        return students[id]