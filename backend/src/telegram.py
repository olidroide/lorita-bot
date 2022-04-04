# from telebot.async_telebot import AsyncTeleBot
from aiogram import Bot, Dispatcher, types

from app import Settings


async def init_telegram(config: Settings):
    if not config.domain_name or not config.telegram_api_key or config.testing:
        return

    bot = Bot(token=config.telegram_api_key)


    WEBHOOK_URL = f"https://{config.domain_name}{config.baseurl}/telegram"
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)

    return LoritaTelegram(bot=bot)


class LoritaTelegram:
    bot: Bot
    dispatcher: Dispatcher

    def __init__(
        self,
        bot: Bot
    ) -> None:
        super().__init__()
        self.bot = bot
        dispatcher = Dispatcher(bot)


        @dispatcher.message_handler(commands="start")
        async def start(message: types.Message):
            await message.answer(f"Hi, {message.from_user.full_name}")

        self.dispatcher = dispatcher

    async def close(self):
        await self.bot.delete_webhook(True)
        await self.bot.close()
