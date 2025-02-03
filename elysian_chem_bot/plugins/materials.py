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

from typing import Union, Any, cast

from elysian_chem_bot import db_instance

from pyrogram.client import Client
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from pyrogram.filters import command, create
from pyrogram.enums import MessageMediaType

from elysian_chem_bot.utils import sanitize_message

log: logging.Logger = logging.getLogger(__name__)
msg_to_be_watched: list[tuple[int, list[str]]] = []


async def should_be_handled(_, __, message: Message) -> bool:
    return any([message.reply_to_message.id == x[0] for x in msg_to_be_watched])


async def get_buttons(sections: list[str]) -> list[str]:
    global db_instance
    db_instance.raw_db = cast(dict[str, dict[str, Any]], db_instance.raw_db)

    cur_section: dict[str, dict[str, Any]] = db_instance.raw_db
    for sec in sections:
        cur_section = cur_section[sec]

    return list(cur_section)


@Client.on_message(create(should_be_handled))
async def handle_reply(client: Client, message: Message) -> None:
    sections: list[str] = [x[1] for x in msg_to_be_watched if x[0] == message.reply_to_message.id][0]
    sections.append(message.text)

    if not db_instance.is_sections_exist(sections):
        sections.pop()
        file: tuple[str, str] = db_instance.get_file(sections, message.text)
        await message.reply_document(file[0])
        return

    material_buttons: list[str] = await get_buttons(sections)
    buttons_rows: list[list[Union[KeyboardButton, str]]] = []

    while len(material_buttons) > 0:
        try:
            current_buttons: list[str] = material_buttons[0:2]
            converted: list[Union[KeyboardButton, str]] = [KeyboardButton(x) for x in current_buttons]
            material_buttons = material_buttons[2:]
        except IndexError:
            converted: list[Union[KeyboardButton, str]] = [KeyboardButton(material_buttons[0])]
            material_buttons.pop(0)

        buttons_rows.append(converted)

    log.info("[reply handler] rows: %s", buttons_rows)
    if len(buttons_rows) == 0:
        log.warning("empty rows!")
        await message.reply_text("this section is empty!")
        return

    msg = await message.reply_text(
        f"Please use the (now changed) button\nnow in section: __{'/'.join(sections)}__",
        reply_markup=ReplyKeyboardMarkup(buttons_rows),
    )

    msg_to_be_watched.append((msg.id, sections))


@Client.on_message(command(["bahan", "material"]))
async def material(client: Client, message: Message) -> None:
    material_buttons: list[str] = await get_buttons([])
    buttons_rows: list[list[Union[KeyboardButton, str]]] = []

    while len(material_buttons) > 0:
        try:
            current_buttons = material_buttons[0:2]
            btns: list[Union[KeyboardButton, str]] = [KeyboardButton(text=x) for x in current_buttons]
            material_buttons = material_buttons[2:]
        except IndexError:
            btns: list[Union[KeyboardButton, str]] = [KeyboardButton(text=material_buttons[0])]
            material_buttons.pop(0)

        buttons_rows.append(btns)

    log.info("rows: %s", buttons_rows)
    msg = await message.reply_text(
        "Please use the button below to make selection",
        reply_markup=ReplyKeyboardMarkup(buttons_rows),
    )

    msg_to_be_watched.append((msg.id, []))


@Client.on_message(command(["addmaterial", "addbahan"]))
async def add_material(client: Client, message: Message) -> None:
    clean_text: str = await sanitize_message(message.text, ["addmaterial", "addbahan"])
    sections: list[str] = clean_text.split("/")

    if not db_instance.is_sections_exist(sections)[0]:
        log.error("sections '%s' does not exist", sections)
        await message.reply_text("section does not exist")
        return

    if not message.reply_to_message:
        await message.reply_text("reply to a message!")
        return

    if message.reply_to_message.media not in (
        MessageMediaType.DOCUMENT,
        MessageMediaType.PHOTO,
        MessageMediaType.VIDEO,
    ):
        await message.reply_text("invalid media type!")
        return

    # check if it's an album
    try:
        medias: list[Message] = await message.reply_to_message.get_media_group()
    except ValueError:
        medias: list[Message] = [message.reply_to_message]

    for media in medias:
        log.info(
            "adding file '%s', where file id: '%s' file unique id: '%s'",
            media.document.file_name,
            media.document.file_id,
            media.document.file_unique_id,
        )
        db_instance.add_file(sections, media.document.file_name, media.document.file_id, media.document.file_unique_id)

    mantap = [f"__{x.document.file_name}__" for x in medias]
    await message.reply_text(f"added {', '.join(mantap)} to section **{sections}**")
