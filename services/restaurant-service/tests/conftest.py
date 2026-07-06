# ── Import the pytest framework ──────────────────────────────────────────────
# pytest provides test discovery, fixtures, assertions, and the test runner.
#conftest.py is pytest's way of saying:
#"Before running any tests, here are the common objects and setup code that every test can reuse."
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.dependencies.database import get_db
from app.core.config import settings
from app.core.redis_component import redis_client
from fastapi.testclient import TestClient
from app.dependencies.auth import get_current_user
from app.schemas.token_payload import TokenPayload

# ── Import your FastAPI application instance ─────────────────────────────────
# 'app' is the FastAPI() object defined in app/main.py.
# This is the actual ASGI application that TestClient will wrap.
from app.main import app
from app.models import Restaurant

DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

# Create a SQLAlchemy engine connected to the test database
engine = create_engine(DATABASE_URL)

# Create a session factory for test database sessions
# autocommit=False: transactions must be explicitly committed
# autoflush=False: changes won't be auto-flushed before queries
# bind=engine: sessions will use the test engine created above
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture
def db():
    db = TestingSessionLocal()

    yield db

    db.query(Restaurant).delete()

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


@pytest.fixture
def owner_user():

    def override():
        return TokenPayload(
            sub="22222222-2222-2222-2222-222222222222",
            role="RESTAURANT_OWNER"
        )

    app.dependency_overrides[get_current_user] = override

    yield

    app.dependency_overrides.clear()

@pytest.fixture
def owner_customer():
    def override():
        return TokenPayload(
            sub="22222222-2222-2222-2222-222222222222",
            role="CUSTOMER"
        )
    app.dependency_overrides[get_current_user] = override

    yield

    app.dependency_overrides.clear()