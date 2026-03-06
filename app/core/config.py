from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Any
import os
from dotenv import load_dotenv  # Опционально, fallback

load_dotenv() 

class Setting(BaseSettings):
    host: str
    port: int
    max_users: int

    db_user: str
    db_password: str
    db_port: str
    db_host: str
    db_name: str
    time_interval_minutes: int

    secret_key: str
    algorithm: str
    access_token_expire_minutes:int

    hh_base_url: str
    hh_api_key: str
    parser_interval_seconds: int
    per_page: int

    encoding: str
    debug: bool
    app_name: str

    def get_hh_headers(self):
        return {
            "User-Agent": self.app_name, "Authorization": f"Bearer {self.hh_api_key}"
        }

    def async_database_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    def sync_database_url(self):
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    model_config = SettingsConfigDict(
        env_file=".env",              # Загрузка из .env в корне
        env_file_encoding="utf-8",    # Кодировка
        env_ignore_empty=True,        # Пустые vars = default
        extra="ignore",               # Лишние vars игнор
        case_sensitive=False          # python -> PYTHON_HOST
    )

settings = Setting()