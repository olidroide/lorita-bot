from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    baseurl: str = "/api/v1"
    port: int = 8000
    log_level: str = "DEBUG"
    twilio_account_sid: str
    twilio_auth_token: str
    dg_key: str

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        env_prefix = "LORITA_BOT_BACKEND_"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
