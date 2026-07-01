# ── Import the pytest framework ──────────────────────────────────────────────
# pytest provides test discovery, fixtures, assertions, and the test runner.
#conftest.py is pytest's way of saying:
#"Before running any tests, here are the common objects and setup code that every test can reuse."
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.dependencies.database import get_db
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.config import settings
from app.core.redis_com import redis_client

# ── Import FastAPI's built-in test HTTP client ───────────────────────────────
# TestClient wraps your FastAPI app so you can make real HTTP calls
# (GET, POST, etc.) without actually starting a server.
from fastapi.testclient import TestClient

# ── Import your FastAPI application instance ─────────────────────────────────
# 'app' is the FastAPI() object defined in app/main.py.
# This is the actual ASGI application that TestClient will wrap.
from app.main import app

DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture
def db():
    db = TestingSessionLocal()

    yield db

    db.query(RefreshToken).delete()
    db.query(User).delete()

    db.commit()
    db.close()
    redis_client.flushdb()



@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()