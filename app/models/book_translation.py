from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database.db import Base

class BookTranslation(Base):
    __tablename__ = "book_translations"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    language_code = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)