from pydantic import BaseModel, HttpUrl
from datetime import datetime

"""Defines what comes in and out of the API"""

class ShortenRequest(BaseModel):
    url: HttpUrl # Pydantic validates this is a real URL

class ShortenResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str

class StatsResponse(BaseModel):
    short_code: str
    original_url: str
    clicks: int
    created_at: datetime
    