import os
from pydantic_settings import BaseSettings, SettingsConfigDict
print("Current Working Directory:", os.getcwd())
ENV_FILE = os.getenv('ENV_FILE', ".env")
print("Current Working Directory:", os.getcwd())
print("Looking for .env at:", os.path.abspath(ENV_FILE))

class Settings(BaseSettings):
    DB_HOST:str
    DB_PORT:int
    DB_USER:str
    DB_PASSWORD:str
    DB_NAME:str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    REDIS_HOST:str
    REDIS_PORT:int

    APP_NAME:str
    APP_VERSION:str

    RESTAURANT_SERVICE_URL:str

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra='ignore')

settings = Settings()
