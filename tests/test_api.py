import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal, redis_client
from app import models
import sqlalchemy
from fastapi import HTTPException

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    # Drop all tables to ensure a clean slate
    Base.metadata.drop_all(bind=engine)
    # Create all tables based on models with the unique constraint
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        books_to_add = [
            {"title": "Pride and Prejudice", "author": "Jane Austen"},
            {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
            {"title": "Animal Farm", "author": "George Orwell"},
            {"title": "Jane Eyre", "author": "Charlotte Brontë"},
            {"title": "The Catcher in the Rye", "author": "J.D. Salinger"},
            {"title": "Brave New World", "author": "Aldous Huxley"},
            {"title": "Lord of the Rings", "author": "J.R.R. Tolkien"},
            {"title": "The Hobbit", "author": "J.R.R. Tolkien"}  # Unique title, same author
        ]
        added_count = 0
        for book in books_to_add:
            response = client.post("/books", json=book)
            if response.status_code == 200:
                added_count += 1
                print(f"Added: {book['title']} by {book['author']}")
            else:
                print(f"Skipped (exists): {book['title']} by {book['author']} - {response.json()['detail']}")
        db.commit()  # Not needed with API, but kept for consistency
        print(f"Total added: {added_count}")
        assert added_count == 8, f"Expected 8 unique books, got {added_count}"
    finally:
        db.close()
    yield
    # Teardown: Drop all tables
    Base.metadata.drop_all(bind=engine)
    redis_client.flushdb()  # Clear Redis cache

def test_get_books(setup_database):
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 8  # 8 unique books
    titles = [book["title"] for book in data]
    assert "Pride and Prejudice" in titles
    assert "The Hobbit" in titles

def test_post_books_success(setup_database):
    new_book = {"title": "New Unique Book", "author": "New Unique Author"}
    response = client.post("/books", json=new_book)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Unique Book"
    assert data["author"] == "New Unique Author"
    assert "id" in data

    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 9  # 8 initial + 1 new

def test_post_books_duplicate(setup_database):
    duplicate_book = {"title": "Animal Farm", "author": "George Orwell"}
    response = client.post("/books", json=duplicate_book)
    assert response.status_code == 400
    assert response.json()["detail"] == "Book already exists"

def test_post_books_missing_fields(setup_database):
    invalid_book = {"title": "Missing Author"}  # Missing author
    response = client.post("/books", json=invalid_book)
    assert response.status_code == 422  # Updated to match Pydantic validation
    assert "detail" in response.json()  # Ensure error message is present

def test_post_books_server_error(setup_database):
    invalid_book = {"title": 123, "author": "Test"}  # Invalid type for title
    response = client.post("/books", json=invalid_book)
    assert response.status_code == 422  # Unprocessable Entity