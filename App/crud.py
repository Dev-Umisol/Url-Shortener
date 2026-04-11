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
    
    db_url = models.URL(original_url=original_url, short_code=code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    return db_url
    
    