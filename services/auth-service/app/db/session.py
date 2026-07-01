from app.core.config import settings        # Import app-specific settings (DB credentials, etc.)
from sqlalchemy import create_engine        # Function to create a DB engine (connection pool)
from sqlalchemy.orm import sessionmaker     # Factory for creating DB session objects

# Build the PostgreSQL connection string using credentials from settings
DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:"    # DB username
    f"{settings.DB_PASSWORD}@"             # DB password
    f"{settings.DB_HOST}:"                 # Hostname or IP of the DB server
    f"{settings.DB_PORT}/"                 # Port (default Postgres: 5432)
    f"{settings.DB_NAME}"                  # Target database name
)

print(
    settings.DB_HOST,
    settings.DB_PORT,
    settings.DB_NAME
)

# Create the SQLAlchemy engine; echo=True logs all SQL queries to console
engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory; autocommit/autoflush=False gives manual control over transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)