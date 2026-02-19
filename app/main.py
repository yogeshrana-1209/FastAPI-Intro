import uvicorn
import os
import uuid
import aiofiles
# from fastapi import FastAPI, Path, Query
from fastapi import FastAPI, Body, Request, File, UploadFile, Cookie, Header
from fastapi.responses import HTMLResponse
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Form
from fastapi.responses import JSONResponse   
from app.routers import model
from app.routers import nestedmodel
from app.routers import depinjection_example
from app.routers import bookrouter
import shutil
# from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

#Import Other Files routes from (/routes folder)
app.include_router(model.router)
app.include_router(nestedmodel.router)
app.include_router(depinjection_example.router)
app.include_router(bookrouter.router, prefix="/api/v1", tags=["Books"])

#variables
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# print("BaseModel", BaseModel)
# Get greet msg
@app.get("/")
async def index():
   return {"message": "Hello, Welcome to FastAPI Tutorial"}

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

@app.get("/hellomsg/{name}", response_class=HTMLResponse)
async def hellomsg(request: Request, name:str):
   return templates.TemplateResponse("hellomsg.html", {"request": request, "name":name})

# Method=1 (Using HTML Form)
#Submit Form using html Form
@app.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
   return templates.TemplateResponse("login.html", {"request": request})

#Submit Form using html Form
@app.post("/submit/")
async def submit(nm: str = Form(...), pwd: str = Form(...)):
   return {"username": nm}

#Method=2 (Using Pydantic Model)

class User(BaseModel):
   username: str
   password: str

@app.post("/submit/", response_model=User)
async def submit(nm: User = Form(...), pwd: str = Form(...)):
   return User(username=nm, password=pwd)

# File Upload API (Front-end)
@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
   return templates.TemplateResponse("uploadfile.html", {"request": request})

# Upload File (Create File Upload api)
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
   with open("destination.png", "wb") as buffer:
      shutil.copyfileobj(file.file, buffer)
   return {"filename": file.filename}  

@app.post("/fileupload/")
async def upload_file(file: UploadFile = File(...)):

    file_ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    return {
        "original_name": file.filename,
        "saved_as": unique_name
    }

# Set Cookie api
@app.post("/cookie/")
def create_cookie():
   content = {"message": "cookie set"}
   response = JSONResponse(content=content)
   response.set_cookie(key="username", value="yogesh")
   return response

# Get/Read Cookie
@app.get("/readcookie/")
async def read_cookie(username: str = Cookie(None)):
   return {"username": username}

#Header Parameters
@app.get("/headers/")
async def read_header(accept_language: Optional[str] = Header(None)):
   return {"Accept-Language": accept_language} 

#Change the Response Headers
@app.get("/rspheader/")
def set_rsp_headers():
   content = {"message": "Hello World"}
   headers = {"X-Web-Framework": "FastAPI", "Content-Language": "en-US"}
   return JSONResponse(content=content, headers=headers)