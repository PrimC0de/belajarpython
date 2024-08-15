import http

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.infrastructures.databases.database import postgres, get_db
from src.schemas.book_schemas import BookCreate, BookUpdate, BookResponse
from src.crud.book_crud import create_book, update_book, delete_book, get_book, get_books
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.domains.auth.entities.book import Book
from src.domains.auth.auth_http import router as auth_router
from src.router.book_router import router as book_routers

app = FastAPI(title="OBP RBP Backend")


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/books/", response_model=BookResponse)
async def create_book_route(book: BookCreate, db: Session = Depends(get_db)):
    existing_book = get_book(db, isbn=book.isbn)
    if existing_book:
        raise HTTPException(status_code=400, detail="ISBN already registered")
    return create_book(db=db, book=book)

@app.get("/api/books/{book_id}", response_model=BookResponse)
async def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.get("/api/books/", response_model=list[BookResponse])
async def read_books(db: Session = Depends(get_db)):
    return get_books(db)

@app.put("/api/books/{book_id}", response_model=BookResponse)
async def update_book_route(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return update_book(db=db, book_id=book_id, book=book)

@app.delete("/api/books/{book_id}", status_code=204)
async def delete_book_route(book_id: int, db: Session = Depends(get_db)):
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    delete_book(db=db, book_id=book_id)
    return None

@app.get("/api/force_error")
async def force_error():
    raise HTTPException(status_code=500, detail="Forced error")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=http.HTTPStatus.BAD_REQUEST,
        content=jsonable_encoder(
            {
                "error": " ".join([str(i) for i in exc.errors()[0]['loc']]) + " " + exc.errors()[0]["msg"],
                "status_code": http.HTTPStatus.BAD_REQUEST,
            }
        ),
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    err = " ".join([str(i) for i in exc.errors()[0]['loc']])
    return JSONResponse(
        status_code=http.HTTPStatus.BAD_REQUEST,
        content=jsonable_encoder(
            {
                "error": err + ": " + exc.errors()[0]["msg"],
                "status_code": http.HTTPStatus.BAD_REQUEST,
            }
        ),
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"error": exc.detail, "status_code": exc.status_code}),
    )


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({"status_code": 500, "error": str(exc)}),
    )


app.include_router(auth_router)
app.include_router(book_routers)