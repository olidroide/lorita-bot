from telebot.async_telebot import AsyncTeleBot

from app import Settings


async def init_telegram(config: Settings):
    bot = AsyncTeleBot(config.telegram_api_key)
    await bot.polling()

    # Handle '/start' and '/help'
    @bot.message_handler(commands=["help", "start"])
    async def send_welcome(self, message):
        await self.bot.reply_to(
            message,
            """\
    Hi there, I am EchoBot.
    I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
    """,
        )

    # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
    @bot.message_handler(func=lambda message: True)
    async def echo_message(self, message):
        await self.bot.reply_to(message, message.text)

    return bot

#
# class LoritaTelegram:
#     bot: AsyncTeleBot
#
#     def __init__(self, bot: AsyncTeleBot) -> None:
#         super().__init__()
#         self.bot = bot


