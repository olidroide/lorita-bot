import os
from functools import lru_cache

from fastapi import FastAPI
from pydantic import BaseSettings
from twilio.rest import Client  # type: ignore


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "LORITA_BOT_"
        case_sensitive = False

    debug: bool = False
    baseurl: str = "/"
    log_level: str = "DEBUG"
    twilio_account_sid: str
    twilio_auth_token: str
    dg_key: str


@lru_cache()
def get_settings() -> Settings:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return Settings(_env_file=os.path.join(dir_path, "..", ".env"))


def create_app():
    config = get_settings()

    app = FastAPI(
        title="⚡ LORITA BOT",
        description="Lorita is like a parrot instead repeat and audio, transcribe it to text",
        version="1.0.0",
        debug=config.debug,
        docs_url="/docs/",
        openapi_url="/docs/openapi.json",
        servers=[{"url": config.baseurl}],
    )

    app.state.config = config

    @app.on_event("startup")
    async def startup_event():
        pass

    @app.on_event("shutdown")
    async def shutdown_event():
        pass

    return app
