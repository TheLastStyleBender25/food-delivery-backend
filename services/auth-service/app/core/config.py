from pydantic_settings import BaseSettings, SettingsConfigDict  # Pydantic library for managing app settings from env variables
import os

ENV_FILE = os.getenv("ENV_FILE", ".env")

class Settings(BaseSettings):  # Inherits BaseSettings — auto-reads values from environment/.env file

    # --- Database Configuration ---
    DB_HOST: str  # Hostname or IP address of the database server
    DB_PORT: int  # Port number (PostgreSQL default: 5432)
    DB_NAME: str  # Name of the database to connect to
    DB_USER: str  # Database login username
    DB_PASSWORD: str  # Database login password

    # --- JWT Authentication Configuration ---
    JWT_SECRET_KEY: str  # Secret key used to sign/verify JWT tokens (keep this private!)
    JWT_ALGORITHM: str  # Hashing algorithm for JWT (e.g. "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int  # How long an access token stays valid (in minutes)
    REFRESH_TOKEN_EXPIRE_DAYS: int  # How long a refresh token stays valid (in days)
    RATE_LIMIT: str

    REDIS_HOST: str
    REDIS_PORT: int

    RABBITMQ_HOST : str
    RABBITMQ_PORT : int

    EMAIL_VERIFICATION_EXPIRE_HOURS: int

    OTP_EXPIRATION_SECONDS:int

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,  # Tells pydantic to load values from a .env file
        extra="ignore"  # Silently ignores any extra variables in .env not defined above
    )


settings = Settings()  # Creates a single shared instance — import this anywhere in the app to access config
