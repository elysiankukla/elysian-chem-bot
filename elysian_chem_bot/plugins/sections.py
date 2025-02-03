import logging
import traceback

from elysian_chem_bot import db_instance
from elysian_chem_bot.utils import sanitize_message

from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram.filters import command

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(command("addsections"))
async def add_sections(client: Client, message: Message):
    clean_text: str = await sanitize_message(message.text, "addsections")
    sections: list[str] = clean_text.split("/")

    log.info("adding sections: %s", sections)
    msg = await message.reply_text("__Adding sections...__")
    try:
        db_instance.add_section(sections)
        log.info("successful")
        await msg.edit_text("**Successfully** added.")
    except Exception as e:
        log.error("failed to add section, exception: %s", e)
        await msg.edit_text(f"**Failed** to add sections! error:\n```\n{traceback.format_exc()}\n```")


@Client.on_message(command("removesections"))
async def remove_sections(client: Client, message: Message) -> None:
    clean_text: str = await sanitize_message(message.text, "removesections")
    sections: list[str] = clean_text.split("/")

    log.info("removing sections: %s", sections)
    msg = await message.reply_text("__Removing sections...__")

    try:
        db_instance.remove_section(sections)
        log.info("successful")
        await msg.edit_text("**Successfully** removed.")
    except Exception as e:
        log.error("failed to remove section, exception: %s", e)
        await msg.edit_text(f"**Failed** to remove sections! error:\n```\n{traceback.format_exc()}\n```")
