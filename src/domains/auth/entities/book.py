from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column, MappedColumn, relationship

from src.shared.entities.basemodel import BaseModel
from src.validators.validator import Validator

class Book(BaseModel):
    __tablename__ = "books"

    id: MappedColumn[int] = mapped_column(Integer, primary_key = True, index = True)
    name: MappedColumn[str] = mapped_column(String, index = True)
    isbn: MappedColumn[str] = mapped_column(String, unique = True)
    author: MappedColumn[str] = mapped_column(String)
