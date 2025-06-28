# PreduskTA - Books API 🎉📚
Welcome to PreduskTA, a vibrant FastAPI-based REST API application designed to manage a delightful collection of books with a unique constraint on the combination of title and author. This project features a SQLite database managed with Alembic migrations, Redis caching, a review system for books, and comprehensive unit tests using pytest. Let’s get started! 🌟
## Features ✨

- ***GET /books***: Fetch all books, cached with Redis for 5 minutes ⏳.
- ***POST /books***: Add a new book with validation for duplicates, missing fields, and invalid data types ✅.
- ***GET /books/{book_id}/reviews***: Retrieve reviews for a specific book 📝.
- ***POST /books/{book_id}/reviews***: Add a review (rating and comment) for a book with validation ⭐.
- ***Error Handling***: Returns appropriate HTTP status codes (e.g., 400 for duplicates, 422 for validation errors, 500 for server errors) 🚨.
- ***Testing***: Includes pytest tests for all endpoints and edge cases 🧪.
- ***Migrations***: Uses Alembic to manage database schema changes 🛠️.
---
## Prerequisites 🛠️

- Python 3.10 or higher 🐍
- Git (for version control) 📊
- Redis server (for caching, optional for local testing with a fallback) 🗃️
- A passion for coding and books! 📖
---
## Installation 🚀
### 1. Set Up a Virtual Environment 🌱
```base
python -m venv venv
venv\Scripts\activate  # On Windows 😊
# source venv/bin/activate  # On macOS/Linux 🌴
```
### 2. Install Dependencies 📦
```bash 
Install the required Python packages:
pip install -r requirements.txt
```
If requirements.txt is not present, create it with:
```bash
pip freeze > requirements.txt
```
Ensure these packages are included (or install manually):
```bash
fastapi
uvicorn
sqlalchemy
alembic
pydantic
redis
python-dotenv  # For loading .env file
pytest
pytest-asyncio
```
### 3. Set Up the Database and Migrations 🗄️

- The app uses a SQLite database file named ***preduskTA.db*** in the project root.

- Set up Alembic migrations:
### Initialize Alembic 🌱

<pre>alembic init migrations</pre>


- Edit migrations/env.py to ```import Base from app.models``` and ```set target_metadata = Base.metadata```.
- Update alembic.ini with the SQLite URL: ```sqlalchemy.url = sqlite+pysqlite:///./preduskTA.db```.
---
## Create a Migration 📝
Generate a migration script for the books and reviews tables:
<pre>alembic revision -m "create books and reviews tables with constraints"</pre>

## Apply Migrations 🎉
<pre>alembic upgrade head</pre>


This creates the preduskTA.db file with the books and reviews tables.



### 4. Configure Redis 🔧

Create a .env file in the project root to store your Redis URL:<pre>REDIS_URL=redis://localhost:6379  # Default for local testing, replace with your Redis instance URL</pre>


Load the .env file in app/database.py by adding these lines at the top:
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Replace the redis_url line with:
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")  # Fallback to local if not set
```

- Ensure a Redis server is running locally or accessible at the URL in the .env file.
- Add .env to .gitignore to keep sensitive data secure:.env



## Running the Application 🎬
### 1. Start the Server 🚀
Activate the virtual environment and run the FastAPI app with uvicorn:
```uvicorn app.main:app --reload --log-level debug```


- Access the app at ```http://127.0.0.1:8000```.
- --reload enables auto-reloading on code changes.
- --log-level debug provides detailed logs for troubleshooting.

### 2. Access API Documentation 📖

FastAPI automatically generates interactive Swagger documentation. Once the server is running, open your browser and navigate to:
```bash
http://127.0.0.1:8000/docs
```
- Explore endpoints, try out requests, and view response schemas directly in the browser! 🌐
### 3. Test the API 🌐
Try the endpoints with curl, Postman, or a browser:

- GET /books: 
```bash
curl http://127.0.0.1:8000/books
```


- POST /books:
```bash
curl -X POST http://127.0.0.1:8000/books -H "Content-Type: application/json" -d "{\"title\": \"New Book\", \"author\": \"New Author\"}"
```


- GET /books/{book_id}/reviews:
```bash
curl http://127.0.0.1:8000/books/1/reviews
```


- POST /books/{book_id}/reviews:
```bash
curl -X POST http://127.0.0.1:8000/books/1/reviews -H "Content-Type: application/json" -d "{\"rating\": 4, \"comment\": \"Great read!\"}"
```



## Running Tests 🧪
### 1. Run Tests ✅
Activate the virtual environment and execute:
<pre>pytest tests/ -v</pre>


- -v gives verbose output.
- Tests manage the preduskTA.db file with migrations.

### 2. Check Test Coverage 📊
Install pytest-cov and run:
<pre>pip install pytest-cov
pytest tests/ --cov=app --cov-report=html
</pre>
Open htmlcov/index.html in a browser to see coverage results.
## Project Structure 🗂️
<pre>
preduskTA/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── routes.py
├── migrations/
│   ├── env.py
│   └── versions/
├── tests/
│   └── test_api.py
├── requirements.txt
├── preduskTA.db  (generated on first run)
├── .env    (configuration file, add to .gitignore)
├── alembic.ini          
└── README.md

</pre>
--- 
## Troubleshooting ⚠️

- 500 Errors: Review server logs. Ensure the database is writable, migrations are applied, and Redis is accessible.
- Test Failures: Delete preduskTA.db and rerun tests. Check migrations with alembic current.
- Migration Issues: Verify alembic.ini URL and env.py metadata.
- Redis Issues: Confirm REDIS_URL in .env or start a local Redis server.

## Contributing 🤝
We’d love your input! Submit issues or pull requests on the GitHub repository. 🌈