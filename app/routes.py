from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database
import json
from pydantic import BaseModel, Field, ConfigDict
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Pydantic model for validation
class BookCreate(BaseModel):
    title: str = Field(..., description="Title of the book")
    author: str = Field(..., description="Author of the book")

    model_config = ConfigDict(
        json_schema_extra={"example": {"title": "Sample Book", "author": "Sample Author"}}
    )

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in session: {str(e)}")
        raise  # Re-raise to let the endpoint handle it
    finally:
        db.close()

@router.post("/books", response_model=dict)
async def add_book(book: BookCreate, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Checking for existing book: {book.title} by {book.author}")
        existing_book = db.query(models.Book).filter_by(title=book.title, author=book.author).first()
        if existing_book:
            logger.debug("Duplicate book found")
            raise HTTPException(status_code=400, detail="Book already exists")
        logger.debug("No duplicate found, proceeding with insertion")
        db_book = models.Book(**book.model_dump())
        db.add(db_book)
        db.commit()
        logger.debug("Commit successful")
        db.refresh(db_book)
        database.redis_client.delete("books_cache")  # Invalidate cache
        return {"id": db_book.id, "title": db_book.title, "author": db_book.author}
    except HTTPException as http_err:
        logger.debug(f"HTTPException raised: {str(http_err)}")
        raise http_err
    except ValueError as ve:
        logger.error(f"ValueError: {str(ve)}")
        raise HTTPException(status_code=422, detail=f"Invalid data: {str(ve)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.get("/books", response_model=list)
async def get_books(db: Session = Depends(get_db)):
    cache_key = "books_cache"
    cached_data = database.redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    try:
        books = db.query(models.Book).all()
        data = [{"id": book.id, "title": book.title, "author": book.author} for book in books]
        database.redis_client.setex(cache_key, 300, json.dumps(data))  # Cache for 5 minutes
        return data
    except Exception as e:
        logger.error(f"Failed to retrieve books: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve books: {str(e)}")

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