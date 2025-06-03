from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import final


@final
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env'),
        env_file_encoding='utf-8',
        extra='ignore')

    database_url: str = 'postgresql+asyncpg://postgres:1234@localhost:5432/database'
    redis_url: str = 'redis://localhost:6379/0'
    api_key: str = ''
    auth_token: str = ''
    
@lru_cache()  # get it from memory
def get_settings() -> Settings:
    return Settings()
