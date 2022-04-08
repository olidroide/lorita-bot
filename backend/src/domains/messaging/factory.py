from contextlib import asynccontextmanager
from typing import AsyncIterator

from app import get_settings
from .telegram import LoritaTelegram

config = get_settings()


@asynccontextmanager
async def get_telegram_client() -> AsyncIterator[LoritaTelegram]:
    if config.testing:
        telegram_client = await LoritaTelegram.create(
            api_key="0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            config=config,
        )
    else:
        if not config.domain_name or not config.telegram_api_key:
            return

        telegram_client = await LoritaTelegram.create(api_key=config.telegram_api_key, config=config)

    yield telegram_client
