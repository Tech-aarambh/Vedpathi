from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base


class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)

    language_code = Column(String, nullable=False)  # hi, mr, en
    translated_text = Column(Text, nullable=False)

    verse_id = Column(Integer, ForeignKey("verses.id"), nullable=False)

    verse = relationship("Verse")