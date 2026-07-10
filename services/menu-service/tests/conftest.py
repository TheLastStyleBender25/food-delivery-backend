import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings
from app.core.redis_component import redis_client
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.main import app
from app.schemas.token_payload import TokenPayload

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

# Create one loop for the entire test session
_event_loop = asyncio.new_event_loop()


@pytest.fixture(scope="session")
def event_loop():
    """Override pytest-asyncio's loop with a single session-scoped one."""
    yield _event_loop
    _event_loop.close()


# Create engine and session factory once, outside any fixture,
# so they're bound to the module-level loop above
_engine = create_async_engine(DATABASE_URL, future=True)
_session_factory = async_sessionmaker(
    bind=_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=True,
)


@pytest_asyncio.fixture(scope="function")
async def db():
    async with _session_factory() as session:
        yield session
        await session.rollback()
    await redis_client.flushdb()


@pytest_asyncio.fixture(scope="function")
async def client(db):
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def owner_user():
    def override():
        return TokenPayload(
            sub="22222222-2222-2222-2222-222222222222",
            role="RESTAURANT_OWNER",
        )
    app.dependency_overrides[get_current_user] = override
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def owner_customer():
    def override():
        return TokenPayload(
            sub="22222222-2222-2222-2222-222222222222",
            role="CUSTOMER",
        )
    app.dependency_overrides[get_current_user] = override
    yield
    app.dependency_overrides.clear()