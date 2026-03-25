from app.models.book import Book
from app.models.section import Section



from app.models.translation import Translation

from pydantic import BaseModel
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.verse import Verse

router = APIRouter(prefix="/verses", tags=["Verses"])


@router.post("/create")
def create_verse(
    section_id: int,
    verse_number: int,
    sanskrit_text: str,
    db: Session = Depends(get_db)
):
    new_verse = Verse(
        section_id=section_id,
        verse_number=verse_number,
        sanskrit_text=sanskrit_text
    )

    db.add(new_verse)
    db.commit()
    db.refresh(new_verse)

    return new_verse


@router.get("/by-section/{section_id}")
def get_verses_by_section(section_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Verse)
        .filter(Verse.section_id == section_id)
        .order_by(Verse.verse_number)
        .all()
    )


    from pydantic import BaseModel
from typing import List


class VerseCreate(BaseModel):
    verse_number: int
    sanskrit_text: str


class BulkVerseCreate(BaseModel):
    section_id: int
    verses: List[VerseCreate]


@router.post("/bulk-create")
def bulk_create_verses(data: BulkVerseCreate, db: Session = Depends(get_db)):
    created_verses = []

    for verse in data.verses:
        new_verse = Verse(
            section_id=data.section_id,
            verse_number=verse.verse_number,
            sanskrit_text=verse.sanskrit_text
        )
        db.add(new_verse)
        created_verses.append(new_verse)

    db.commit()

    return {
        "message": f"{len(created_verses)} verses inserted successfully"
    }

@router.put("/update/{verse_id}")
def update_verse(
    verse_id: int,
    sanskrit_text: str,
    db: Session = Depends(get_db)
):
    verse = db.query(Verse).filter(Verse.id == verse_id).first()

    if not verse:
        return {"error": "Verse not found"}

    verse.sanskrit_text = sanskrit_text
    db.commit()
    db.refresh(verse)

    return verse




class TranslationCreate(BaseModel):
    verse_id: int
    language_code: str
    translated_text: str


class BulkTranslationCreate(BaseModel):
    translations: List[TranslationCreate]


@router.post("/bulk-translate")
def bulk_add_translations(data: BulkTranslationCreate, db: Session = Depends(get_db)):
    created = []

    for item in data.translations:
        new_translation = Translation(
            verse_id=item.verse_id,
            language_code=item.language_code,
            translated_text=item.translated_text
        )
        db.add(new_translation)
        created.append(new_translation)

    db.commit()

    return {
        "message": f"{len(created)} translations inserted successfully"
    }

@router.get("/with-translation/{section_id}")
def get_verses_with_translation(
    section_id: int,
    language_code: str,
    db: Session = Depends(get_db)
):
    verses = (
        db.query(Verse)
        .filter(Verse.section_id == section_id)
        .order_by(Verse.verse_number)
        .all()
    )

    result = []

    for verse in verses:
        translation = (
            db.query(Translation)
            .filter(
                Translation.verse_id == verse.id,
                Translation.language_code == language_code
            )
            .first()
        )

        result.append({
            "verse_number": verse.verse_number,
            "sanskrit_text": verse.sanskrit_text,
            "translation": translation.translated_text if translation else None
        })

    return result


@router.get("/search")
def search_verses(query: str, db: Session = Depends(get_db)):

    verses = db.query(Verse).filter(
        Verse.sanskrit_text.contains(query)
    ).all()

    results = []

    for verse in verses:

        section = db.query(Section).filter(Section.id == verse.section_id).first()
        book = db.query(Book).filter(Book.id == section.book_id).first()

        results.append({
            "book_title": book.title,
            "section_title": section.title,
            "verse_number": verse.verse_number,
            "sanskrit_text": verse.sanskrit_text
        })

    return results