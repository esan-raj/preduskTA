from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import redis
import os
from dotenv import load_dotenv
load_dotenv()
SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///./preduskTA.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

# Redis configuration using Railway environment variable
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")  # Fallback for local testing
redis_client = redis.Redis.from_url(redis_url)

Base = declarative_base()