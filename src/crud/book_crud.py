from sqlalchemy.orm import Session
from src.domains.auth.entities.book import Book
from src.schemas.book_schemas import BookCreate, BookUpdate

def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def update_book(db: Session, book_id: int, book: BookUpdate):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        for key, value in book.dict().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 10, name: str = None, isbn: str = None, author: str = None):
    query = db.query(Book).offset(skip).limit(limit)
    if name:
        query = query.filter(Book.name.like(f"%{name}%"))
    if isbn:
        query = query.filter(Book.isbn == isbn)
    if author:
        query = query.filter(Book.author.like(f"%{author}%"))
    return query.all()