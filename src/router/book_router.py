from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.infrastructures.databases.database import get_db
from src.schemas.book_schemas import BookCreate, BookUpdate, BookResponse
from src.crud.book_crud import create_book, update_book, delete_book, get_book, get_books

router = APIRouter()

@router.post("/books/", response_model=BookResponse)
def create_book_endpoint(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book)

@router.put("/books/{book_id}", response_model=BookResponse)
def update_book_endpoint(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = update_book(db, book_id, book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.delete("/books/{book_id}", response_model=BookResponse)
def delete_book_endpoint(book_id: int, db: Session = Depends(get_db)):
    db_book = delete_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.get("/books/", response_model=list[BookResponse])
def list_books(skip: int = 0, limit: int = 10, isbn: str = None, author: str = None, name: str = None, db: Session = Depends(get_db)):
    return get_books(db, skip, limit, isbn, author, name)

@router.get("/books/{book_id}", response_model=BookResponse)
def get_book_endpoint(book_id: int, db: Session = Depends(get_db)):
    db_book = get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

