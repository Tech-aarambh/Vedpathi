from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base


class Verse(Base):
    __tablename__ = "verses"

    id = Column(Integer, primary_key=True, index=True)
    verse_number = Column(Integer, nullable=False)
    sanskrit_text = Column(Text, nullable=False)

    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)

    section = relationship("Section")