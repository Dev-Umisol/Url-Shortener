import random
import string
from sqlalchemy.orm import Session
from App import models

"""Contains all database opertions, makes the code testable and reusable"""

def generate_code(length: int = 6) -> str:
    """Generates a random short code of given length"""
    chars = string.ascii_letters + string.digits
    
    return "".join(random.choices(chars, k=length))

def create_short_url(db: Session, original_url: str) -> models.URL:
    """Creates a new short URL entry in the database"""
    
    # Generate a unique code (retry if collision occurs)
    while True:
        code = generate_code()
        
        if not db.query(models.URL).filter(models.URL.short_code == code).first():
            break
    
    db_url = models.URL(original_url=original_url, short_code=code) # Create a new URL object
    db.add(db_url) # <-- new row
    db.commit() # <-- save to database
    db.refresh(db_url) # <-- get the generated ID and other fields
    
    return db_url
    
# Returns none if no row matches
def get_url_by_code(db: Session, code: str) -> models.URL | None:
    return db.query(models.URL).filter(models.URL.short_code == code).first()

def increment_clicks(db: Session, url: models.URL) -> None:
    url.clicks += 1
    db.commit()
    