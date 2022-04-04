from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    testing: bool = False
    debug: bool = False
    baseurl: str = "/api/v1"
    port: int = 8000
    log_level: str = "DEBUG"
    twilio_account_sid: Optional[str]
    twilio_auth_token: Optional[str]
    dg_key: Optional[str]
    telegram_api_key: str

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        env_prefix = "LORITA_BOT_BACKEND_"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
