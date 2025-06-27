from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import fakeredis

# SQLite database (for simplicity, can switch to PostgreSQL)
SQLALCHEMY_DATABASE_URL = "sqlite:///./preduskTA.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Mock Redis setup
redis_client = fakeredis.FakeRedis()