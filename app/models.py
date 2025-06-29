from sqlalchemy import Column, Integer, String, ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    __table_args__ = (UniqueConstraint('title', 'author', name='unique_title_author'),)

    reviews = relationship("Review", back_populates="book")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    content = Column(String)
    rating = Column(Integer)

    book = relationship("Book", back_populates="reviews")