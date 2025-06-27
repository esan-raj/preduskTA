from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import database, models
from .database import redis_client
import json

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/books", response_model=list)
async def get_books(db: Session = Depends(get_db)):
    cache_key = "books"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    books = db.query(models.Book).all()
    redis_client.setex(cache_key, 3600, json.dumps([{"id": b.id, "title": b.title, "author": b.author} for b in books]))
    return [{"id": b.id, "title": b.title, "author": b.author} for b in books]

@router.post("/books", response_model=dict)
async def add_book(book: dict, db: Session = Depends(get_db)):
    db_book = models.Book(**book)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {"id": db_book.id, "title": db_book.title, "author": db_book.author}

@router.get("/books/{book_id}/reviews", response_model=list)
async def get_reviews(book_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.book_id == book_id).all()
    return [{"id": r.id, "content": r.content, "rating": r.rating} for r in reviews]

@router.post("/books/{book_id}/reviews", response_model=dict)
async def add_review(book_id: int, review: dict, db: Session = Depends(get_db)):
    db_review = models.Review(book_id=book_id, **review)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return {"id": db_review.id, "content": db_review.content, "rating": db_review.rating}