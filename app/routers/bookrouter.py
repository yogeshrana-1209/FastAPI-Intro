from fastapi import APIRouter
from app.models.bookmodel import Book

router = APIRouter()

data = []

#Add New Book
@router.post("/Books")
def add_book(book: Book):
   data.append(book.dict())
   return data

#Get All Books
@router.get("/Books")
def get_books():
   return data

#Get Single Book
@router.get("/Books/{id}")
def get_book(id: int):
   id = id - 1
   return data[id]

#Update Book
@router.put("/Books/{id}")
def update_book(id: int, book: Book):
   data[id-1] = book
   return data

#Delete Book
@router.delete("/Books/{id}")
def delete_book(id: int):
   data.pop(id-1)
   return data