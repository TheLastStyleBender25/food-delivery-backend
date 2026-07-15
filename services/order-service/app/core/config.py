import os
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = os.getenv("ENV_FILE", ".env")

class Settings(BaseSettings):
    DB_HOST:str
    DB_PORT:int
    DB_USER:str
    DB_NAME:str
    DB_PASSWORD:str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    REDIS_HOST:str
    REDIS_PORT:int

    APP_NAME:str
    APP_VERSION:str

    CART_SERVICE_URL:str
    MENU_SERVICE_URL:str

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra='ignore')

settings = Settings()