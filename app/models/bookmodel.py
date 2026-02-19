from fastapi import APIRouter
from pydantic import BaseModel

#Define Router
router = APIRouter()

#Define Data
data = []

#Define Model
class Book(BaseModel):
   id: int
   title: str
   author: str
   publisher: str