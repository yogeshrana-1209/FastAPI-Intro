import json
from fastapi import APIRouter
from fastapi import APIRouter, HTTPException
from app.models.bookmodel import Book

router = APIRouter()

FILE_PATH = "app/data/books.json"

def read_data():
    with open(FILE_PATH, "r") as f:
        return json.load(f)


def write_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

#Add New Book
@router.post("/Books")
def add_book(book: Book):
   data = read_data()
   data.append(book.dict())
   write_data(data)
   return data

#Get All Books
@router.get("/Books")
def get_books():
   data = read_data()
   return data

#Get Single Book
@router.get("/Books/{id}")
def get_book(id: int):
    data = read_data()
    for book in data:
        if book["id"] == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

#Update Book
@router.put("/Books/{id}")
def update_book(id: int, updated_book: Book):
    data = read_data()
    for index, book in enumerate(data):
        if book["id"] == id:
            data[index] = updated_book.dict()
            write_data(data)
            return data[index]
    raise HTTPException(status_code=404, detail="Book not found")

#Delete Book
@router.delete("/Books/{id}")
def delete_book(id: int):
    data = read_data()
    for index, book in enumerate(data):
        if book["id"] == id:
            deleted = data.pop(index)
            write_data(data)
            return {"message": "Book deleted Successfully", "book": deleted}

    raise HTTPException(status_code=404, detail="Book not found")