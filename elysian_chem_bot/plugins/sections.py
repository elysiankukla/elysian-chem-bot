# SPDX-License-Identifier: Apache-2.0
#
# Copyright 2025 Firdaus Hakimi <hakimifirdaus944@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import traceback

from pyrogram.client import Client
from pyrogram.filters import command
from pyrogram.types import Message

from elysian_chem_bot import db_instance
from elysian_chem_bot.database_types import Sections
from elysian_chem_bot.utils import sanitize_message

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(command("addsections"))
async def add_sections(client: Client, message: Message) -> None:
    clean_text: str = await sanitize_message(message.text, "addsections")
    sections: Sections = clean_text.split("/")

    log.info("adding sections: %s", sections)
    msg = await message.reply_text("__Adding sections...__")
    try:
        db_instance.add_section(sections)
        log.info("successful")
        await msg.edit_text("**Successfully** added.")
    except Exception:
        log.exception("failed to add section, exception:")
        await msg.edit_text(f"**Failed** to add sections! error:\n```\n{traceback.format_exc()}\n```")


@Client.on_message(command("removesections"))
async def remove_sections(client: Client, message: Message) -> None:
    clean_text: str = await sanitize_message(message.text, "removesections")
    sections: Sections = clean_text.split("/")

    log.info("removing sections: %s", sections)
    msg = await message.reply_text("__Removing sections...__")

    try:
        db_instance.remove_section(sections)
        log.info("successful")
        await msg.edit_text("**Successfully** removed.")
    except Exception:
        log.exception("failed to remove section, exception")
        await msg.edit_text(f"**Failed** to remove sections! error:\n```\n{traceback.format_exc()}\n```")
