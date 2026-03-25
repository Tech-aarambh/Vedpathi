from app.models.book_translation import BookTranslation

from fastapi.middleware.cors import CORSMiddleware


from app.api.verse_routes import router as verse_router
from app.api.section_routes import router as section_router
from app.api.book_routes import router as book_router

from fastapi import FastAPI
from app.database.db import Base, engine
from app.api.user_routes import router as user_router

from app.models.book import Book
from app.models.section import Section
from app.models.verse import Verse
from app.models.translation import Translation

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(user_router)
app.include_router(book_router)
app.include_router(section_router)
app.include_router(verse_router)

@app.get("/")
def root():
    return {"message": "Vedpathi API is running"}
