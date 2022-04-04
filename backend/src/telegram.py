# from telebot.async_telebot import AsyncTeleBot
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.webhook import SendMessage

from app import Settings


class LoritaTelegram:
    bot: Bot
    dispatcher: Dispatcher

    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot
        dispatcher = Dispatcher(bot)

        @dispatcher.message_handler(commands="start")
        async def start(message: types.Message):
            await message.answer(f"Hi, {message.from_user.full_name}")

        self.dispatcher = dispatcher

        # @dispatcher.message_handler()
        # async def echo(message: types.Message):
        #     # Regular request
        #     # await bot.send_message(message.chat.id, message.text)
        #
        #     # or reply INTO webhook
        #     return SendMessage(message.chat.id, message.text)

    async def process(self, request, update: dict):
        telegram_update = types.Update(**update)
        Bot.set_current(self.bot)
        await self.dispatcher.process_update(telegram_update)

    async def close(self):
        await self.bot.delete_webhook(True)
        await self.bot.close()


async def init_telegram(config: Settings) -> Optional[LoritaTelegram]:
    if not config.domain_name or not config.telegram_api_key or config.testing:
        return None

    bot = Bot(token=config.telegram_api_key)

    WEBHOOK_URL = f"https://{config.domain_name}{config.baseurl}/telegram"
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)

    return LoritaTelegram(bot=bot)
