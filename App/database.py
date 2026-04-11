from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

""" Creates SQLite connection and gives a session to work with"""

DATABASE_URL = "sqlite:///./shortener.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Dependency to get DB session, FastAPI will call it automatically
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close() # Close connection even it route crashes
        
