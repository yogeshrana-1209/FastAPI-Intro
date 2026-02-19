import uvicorn
# from fastapi import FastAPI, Path, Query
from fastapi import FastAPI, Body, Request
from fastapi.responses import HTMLResponse
from typing import List
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# print("BaseModel", BaseModel)
# Get greet msg
# @app.get("/")
# async def index():
#    return {"message": "Hello World"}

#get name
# @app.get("/helloname/{name}")
# async def hello(name):
#    return {"name": name}

#get name & age
# @app.get("/hello/{name}/{age}")
# async def hello(name:str,age:int):
#    return {"name": name, "age":age}

# get name & age using with Query Params
# @app.get("/hello")
# async def hello(name:str,age:int):
#     return {"name": name, "age": age}

# @app.get("/hello/{name}")
# async def hello(name:str=Path(...,min_length=3, max_length=10)):
#    return {"name": name}

#Vaidation on Params
# @app.get("/users/{name}/{age}")
# async def hello(*, name: str=Path(...,min_length=3 , max_length=10), age: int = Path(..., ge=1, le=100)):
#    return {"name": name, "age":age}

#Validation on Query Parameters
# @app.get("/users/{name}/{age}")
# async def hello(*, name: str=Path(...,min_length=3 ,
# max_length=10), \
#       age: int = Path(..., ge=1, le=100), \
#       percent:float=Query(..., ge=0, le=100)):
#    return {"name": name, "age":age}

class Student(BaseModel):
   id: int
   name :str = Field(None, title="name of student", max_length=10)
   subjects: List[str] = []

@app.post("/students/{college}")
async def student_data(college:str, age:int, student:Student):
   response={"college":college, "age":age, **student.model_dump()}
   return response

@app.get("/greet/")
async def hello():
   response='''
   <html>
   <body>
   <h2>Hello World!</h2>
   </body>
   </html>
   '''
   return HTMLResponse(content=response)

@app.get("/greethtml/", response_class=HTMLResponse)
async def hello(request: Request, name: str):
   return templates.TemplateResponse("greet.html", {"request": request, "name" : name})

if __name__ == "__main__":
   uvicorn.run("main:app", host="localhost", port=8000, reload=True)