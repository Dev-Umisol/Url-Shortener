import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from App.main import app
from App.database import get_db, Base

TEST_DB_URL = "sqlite://"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()
        

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield # Run the test
    Base.metadata.drop_all(bind=engine)
    
client = TestClient(app)

def test_shorten_returns_short_code():
    response = client.post("/shorten/", json={"url": "https://www.example.com"})
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data
    assert len(data["short_code"]) == 6
    
def test_redirect_follows_to_original():
    # First, create a short URL
    post = client.post("/shorten/", json={"url": "https://www.example.com"})
    code = post.json()["short_code"]
    response = client.get(f"/{code}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://www.example.com"
    
def test_stats_increments_clicks():
    # Create a short URL
    post = client.post("/shorten/", json={"url": "https://www.example.com"})
    code = post.json()["short_code"]
    
    # Simulate a redirect
    client.get(f"/{code}", follow_redirects=False)
    # Simulate a redirect again
    client.get(f"/{code}", follow_redirects=False)
    
    # Check initial stats
    stats = client.get(f"/stats/{code}")
    assert stats.json()["clicks"] == 2 # make sure clicks is incremented correctly
    
def test_invalid_url_returns_422():
    response = client.post("/shorten", json={"url": "not-a-valid-url"})
    assert response.status_code == 422
    
def test_missing_code_returns_404():
    response = client.get("/nonexistent", follow_redirects=False)
    assert response.status_code == 404