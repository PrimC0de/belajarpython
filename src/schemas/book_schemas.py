from pydantic import BaseModel, Field

class BookBase(BaseModel):
    name: str
    isbn: str = Field(..., pattern=r'^\d{13}$')
    author: str

class BookCreate(BookBase):
    name: str
    isbn: str
    author: str

class BookUpdate(BaseModel):
    name: str
    isbn: str
    author: str

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True