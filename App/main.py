from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from App import crud, models, schemas
from App.database import engine, get_db

models.Base.metadata.create_all(bind=engine) # Creates the table if it doesn't exist

app = FastAPI(title="Url Shortener")

BASE_URL = "http://localhost:8000/"

