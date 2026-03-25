from app.models.book_translation import BookTranslation

from app.models.book import Book
from app.models.verse import Verse
from app.models.translation import Translation


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.section import Section

router = APIRouter(prefix="/sections", tags=["Sections"])


@router.post("/create")
def create_section(
    book_id: int,
    title: str,
    order_number: int,
    db: Session = Depends(get_db)
):
    new_section = Section(
        book_id=book_id,
        title=title,
        order_number=order_number
    )

    db.add(new_section)
    db.commit()
    db.refresh(new_section)

    return new_section


@router.get("/by-book/{book_id}")
def get_sections_by_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(Section).filter(Section.book_id == book_id).order_by(Section.order_number).all()


@router.put("/update-ending/{section_id}")
def update_section_ending(
    section_id: int,
    ending_text: str,
    db: Session = Depends(get_db)
):
    section = db.query(Section).filter(Section.id == section_id).first()

    if not section:
        return {"error": "Section not found"}

    section.ending_text = ending_text
    db.commit()
    db.refresh(section)

    return section    


@router.get("/full/{section_id}")
def get_full_section(
    section_id: int,
    language_code: str,
    db: Session = Depends(get_db)
):
    # Get section
    section = db.query(Section).filter(Section.id == section_id).first()

    if not section:
        return {"error": "Section not found"}

    # Get book
    book = db.query(Book).filter(Book.id == section.book_id).first()

    book_translation = (
    db.query(BookTranslation)
    .filter(
        BookTranslation.book_id == book.id,
        BookTranslation.language_code == language_code
    )
    .first()
)

    # Get verses
    verses = (
        db.query(Verse)
        .filter(Verse.section_id == section_id)
        .order_by(Verse.verse_number)
        .all()
    )

    verse_list = []

    for verse in verses:
        translation = (
            db.query(Translation)
            .filter(
                Translation.verse_id == verse.id,
                Translation.language_code == language_code
            )
            .first()
        )

        verse_list.append({
            "verse_number": verse.verse_number,
            "sanskrit_text": verse.sanskrit_text,
            "translation": translation.translated_text if translation else None
        })

    return {
        "book_title": book_translation.title if book_translation else book.title,
        "section_title": section.title,
        "ending_text": section.ending_text,
        "verses": verse_list
    }