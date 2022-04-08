import logging

from aiogram import Bot, Dispatcher, types, md
from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware

from app import Settings
from domains.transcription.factory import get_deepgram_client

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0
        logger.debug(f"Middleware counter: {self.counter}")
        super(CounterMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()

        self.counter += 1
        data["counter"] = self.counter
        logger.debug(f"Middleware via on_process_message counter: {data}")

    async def on_process_audio_message(self, message: types.Audio, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()

        self.counter += 1
        data["counter"] = self.counter
        logger.debug(f"Middleware via on_process_audio_message counter: {data}")

    async def on_process_voice_message(self, message: types.Voice, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()

        self.counter += 1
        data["counter"] = self.counter
        logger.debug(f"Middleware via on_process_voice_message counter: {data}")


class LoritaTelegram(object):
    bot: Bot
    dispatcher: Dispatcher

    @classmethod
    async def create(cls, api_key: str, config: Settings):
        bot = Bot(token=api_key, validate_token=not config.testing)
        if not config.testing:
            WEBHOOK_URL = f"https://{config.domain_name}{config.baseurl}/telegram"
            webhook_info = await bot.get_webhook_info()
            if webhook_info.url != WEBHOOK_URL:
                await bot.set_webhook(url=WEBHOOK_URL)

        return LoritaTelegram(bot=bot, config=config)

    def __init__(self, bot: Bot, config: Settings) -> None:
        super().__init__()
        self.bot = bot
        self.config = config
        dispatcher = Dispatcher(self.bot)

        @dispatcher.message_handler(commands="start")
        async def start(message: types.Message):
            await message.answer(f"Hi, {message.from_user.full_name}")
            locale = message.from_user.locale
            await message.reply(
                md.text(
                    md.bold("Info about your language:"),
                    md.text("🔸", md.bold("Code:"), md.code(locale.language)),
                    md.text("🔸", md.bold("Territory:"), md.code(locale.territory or "Unknown")),
                    md.text("🔸", md.bold("Language name:"), md.code(locale.language_name)),
                    md.text("🔸", md.bold("English language name:"), md.code(locale.english_name)),
                    sep="\n",
                )
            )

        @dispatcher.message_handler(content_types=types.ContentType.ANY)
        async def echo(message: types.Message, counter: int):
            # Regular request
            # await bot.send_message(message.chat.id, message.text)

            logger.debug(f"counter from middleware {counter}")
            logger.debug(f"message -> {message}")

            transcribed_text = message.text
            media_url = await message.voice.get_url() if message.voice else None
            media_url = await message.audio.get_url() if message.audio and not media_url else media_url
            logger.debug(f"media URL -> {media_url}")

            if media_url:
                async with get_deepgram_client(api_key=self.config.dg_key) as transcription_client:
                    transcribed_text = await transcription_client.audio_to_text(media_url=media_url)

            try:
                if transcribed_text:
                    await self.bot.send_message(message.chat.id, transcribed_text)
            except Exception as e:
                print(f"{e}")

        self.dispatcher = dispatcher
        self.dispatcher.setup_middleware(CounterMiddleware())

    async def process(self, update: dict):
        telegram_update = types.Update(**update)
        Bot.set_current(self.bot)
        return await self.dispatcher.process_update(telegram_update)

    async def close(self):
        if self.config.testing:
            return

        Bot.set_current(self.bot)
        await self.bot.delete_webhook(True)
        await self.bot.close()
        await self.dispatcher.storage.close()
        await self.dispatcher.storage.wait_closed()
