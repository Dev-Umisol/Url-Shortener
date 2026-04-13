from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from App import crud, models, schemas
from App.database import engine, get_db

models.Base.metadata.create_all(bind=engine) # Creates the table if it doesn't exist

app = FastAPI(title="Url Shortener")

BASE_URL = "http://localhost:8000/"

@app.post("/shorten/", response_model=schemas.ShortenResponse, status_code=201)
def shorten_url(request: schemas.ShortenRequest, db: Session = Depends(get_db)):
    """Endpoint to create a short URL"""
    db_url = crud.create_short_url(db, original_url=str(request.url))
    
    return schemas.ShortenResponse(short_code=db_url.short_code, short_url=f"{BASE_URL}/{db_url.short_code}",
                                   original_url=db_url.original_url,
                                   )
    
@app.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    """Endpoint to redirect to the original URL and increment click count"""
    db_url = crud.get_url_by_code(db, code)
    
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    crud.increment_clicks(db, db_url)
    
    return RedirectResponse(url=db_url.original_url, status_code=307)

@app.get("/stats/{code}", response_model=schemas.StatsResponse)
def get_stats(code: str, db: Session = Depends(get_db)):
    """Endpoint to get statistics for a short URL"""
    db_url = crud.get_url_by_code(db, code)
    
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    return db_url