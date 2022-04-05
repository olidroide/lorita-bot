# from telebot.async_telebot import AsyncTeleBot
from typing import Optional, Callable, Awaitable, Any, Dict

from aiogram import Bot, Dispatcher, types, md
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.webhook import SendMessage

from app import Settings
from domains.transcription.factory import get_deepgram_client


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0
        super(CounterMiddleware, self).__init__()

    async def __call__(
        self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any],
    ) -> Any:
        self.counter += 1
        data["counter"] = self.counter
        print(f"Middleware counter: {data}")
        return await handler(event, data)


class LoritaTelegram:
    bot: Bot
    dispatcher: Dispatcher

    def __init__(self, bot: Bot, config: Settings) -> None:
        super().__init__()
        self.bot = bot
        self.config = config
        dispatcher = Dispatcher(bot)
        dispatcher.setup_middleware(CounterMiddleware())

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

        @dispatcher.message_handler()
        async def echo(message: types.Message):
            # Regular request
            # await bot.send_message(message.chat.id, message.text)
            media_url = await message.audio.get_url()
            transcribed_text = None
            async with get_deepgram_client(api_key=self.config.dg_key) as transcription_client:
                transcribed_text = await transcription_client.audio_to_text(media_url=media_url)

            # or reply INTO webhook
            return SendMessage(message.chat.id, transcribed_text or message.text)

        self.dispatcher = dispatcher

    async def process(self, request, update: dict):
        telegram_update = types.Update(**update)
        Bot.set_current(self.bot)
        await self.dispatcher.process_update(telegram_update)

    async def close(self):
        await self.bot.delete_webhook(True)
        await self.bot.close()
        await self.dispatcher.storage.close()
        await self.dispatcher.storage.wait_closed()


async def init_telegram(config: Settings) -> Optional[LoritaTelegram]:
    if not config.domain_name or not config.telegram_api_key or config.testing:
        return None

    bot = Bot(token=config.telegram_api_key)

    WEBHOOK_URL = f"https://{config.domain_name}{config.baseurl}/telegram"
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)

    return LoritaTelegram(bot=bot, config=config)
