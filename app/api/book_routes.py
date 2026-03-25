from app.models.book_translation import BookTranslation

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.book import Book

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/create")
def create_book(title: str, category: str, description: str = "", db: Session = Depends(get_db)):
    new_book = Book(
        title=title,
        category=category,
        description=description
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


@router.get("/")
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@router.put("/update/{book_id}")
def update_book(
    book_id: int,
    title: str,
    description: str,
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        return {"error": "Book not found"}

    book.title = title
    book.description = description

    db.commit()
    db.refresh(book)

    return book


@router.post("/add-translation")
def add_book_translation(
    book_id: int,
    language_code: str,
    title: str,
    description: str,
    db: Session = Depends(get_db)
):
    new_translation = BookTranslation(
        book_id=book_id,
        language_code=language_code,
        title=title,
        description=description
    )

    db.add(new_translation)
    db.commit()
    db.refresh(new_translation)

    return new_translation