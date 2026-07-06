from pydantic_settings import BaseSettings, SettingsConfigDict
import os

ENV_FILE = os.getenv("ENV_FILE", ".env")
class Settings(BaseSettings):
    APP_NAME: str = "Restaurant Service"
    APP_VERSION: str = "1.0.0"

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    REDIS_HOST : str
    REDIS_PORT : int

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra='ignore')

settings = Settings()