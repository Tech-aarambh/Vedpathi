from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.db import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    order_number = Column(Integer, nullable=False)
    ending_text = Column(Text, nullable=True)

    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    book = relationship("Book")