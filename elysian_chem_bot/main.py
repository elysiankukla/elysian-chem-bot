import elysian_chem_bot.logging  # noqa: F401

from elysian_chem_bot import API_ID, API_HASH, BOT_TOKEN

from pyrogram.client import Client
from pyrogram.types.messages_and_media import Message
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.filters import command


app: Client = Client("elysian_chem_bot", API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


async def start(client: Client, message: Message) -> None:
    await message.reply_text("hi")


def main() -> None:
    app.add_handler(MessageHandler(start, command("start")))
    app.run()
