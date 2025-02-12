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
import zipfile

from typing import Union, Any, cast
from tempfile import NamedTemporaryFile, TemporaryDirectory
from pathlib import Path
from hashlib import sha1

from elysian_chem_bot import db_instance, cmdhelp_instance, DB_PERSIST_PATH

from jsondb.database import JsonDB
from pyrogram.client import Client
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from pyrogram.filters import command, create
from pyrogram.enums import MessageMediaType

from elysian_chem_bot.utils import sanitize_message

log: logging.Logger = logging.getLogger(__name__)
msg_to_be_watched: list[tuple[int, list[str]]] = []
cache_db: JsonDB = JsonDB(Path(Path(DB_PERSIST_PATH).parent).joinpath("extracted_files_cache.json").as_posix())


async def should_be_handled(_, __, message: Message) -> bool:
    if not message.reply_to_message:
        return any([message.chat.id == x[0] for x in msg_to_be_watched])
    return any([message.reply_to_message.id == x[0] for x in msg_to_be_watched])


async def get_buttons(sections: list[str]) -> list[str]:
    global db_instance
    db_instance.raw_db = cast(dict[str, dict[str, Any]], db_instance.raw_db)

    cur_section: dict[str, dict[str, Any]] = db_instance.raw_db
    for sec in sections:
        cur_section = cur_section[sec]

    return list(cur_section)


async def auto_extract_zip_archive(client: Client, message: Message, file_id: str) -> None:
    msg = await message.reply_text("Automatically extracting zip archive...")
    with NamedTemporaryFile() as tf:
        log.info("created temporary file '%s'", tf.name)

        log.info("downloading document with file_id '%s'", file_id)
        await msg.edit_text(f"**downloading document with file_id** `'{file_id}'`")
        await client.download_media(file_id, tf.name)
        log.info("document downloaded")

        with TemporaryDirectory() as td:
            log.info("created temporary directory '%s' for archive extraction", td)
            log.info("**extracting archive**")
            await msg.edit_text("Extracting the zip archive...")
            zipfile.ZipFile(tf.name).extractall(td)
            log.info("archive extracted")

            log.info("uploading extracted files")
            for file in Path(td).rglob("*"):
                if file.is_file():
                    log.info("uploading file '%s'", file.as_posix())
                    await msg.edit_text(f"**uploading file** `'{file.as_posix()}'`")
                    with open(file.as_posix(), "rb") as f:
                        sha1sum: str = sha1(f.read()).hexdigest()
                        if cached_file_id := cache_db.data.get(sha1sum):
                            log.info("file '%s' found in cache, re-using file_id", file.as_posix())
                            await message.reply_document(cached_file_id, file_name=file.name)
                        else:
                            log.info("file '%s' NOT found in cache, uploading instead", file.as_posix())
                            f.seek(0)
                            doc = await message.reply_document(f, file_name=file.name)
                            log.info("storing file '%s' in cache", file.as_posix())
                            cache_db.data.update({sha1sum: doc.document.file_id})

            await msg.delete()


@Client.on_message(create(should_be_handled), group=1)
async def handle_reply(client: Client, message: Message) -> None:
    global msg_to_be_watched

    if message.text.lower() in ["/bahan", "/material"]:
        return

    if message.from_user.id == message.chat.id:
        sections: list[str] = [x[1] for x in msg_to_be_watched if x[0] == message.from_user.id][0]
    else:
        sections: list[str] = [x[1] for x in msg_to_be_watched if x[0] == message.reply_to_message.id][0]
    sections.append(message.text)

    if not db_instance.is_sections_exist(sections)[0]:
        sections.pop()
        file: tuple[str, str] = db_instance.get_file(sections, message.text)
        await message.reply_document(file[0])

        if message.text.endswith(".zip"):
            log.info("file ends with .zip, extracting")
            await auto_extract_zip_archive(client, message, file[0])

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

    if any([message.chat.id == x[0] for x in msg_to_be_watched]):
        rem: list[str] = sections.copy()
        rem.pop()
        msg_to_be_watched = list(filter(lambda x: x[0] != message.from_user.id, msg_to_be_watched))
        msg_to_be_watched.append((message.from_user.id, sections))
    else:
        msg_to_be_watched.append((msg.id, sections))


@Client.on_message(command(["bahan", "material"]))
async def material(client: Client, message: Message) -> None:
    global msg_to_be_watched

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

    if message.chat.id > 0:
        msg_to_be_watched = list(filter(lambda x: x[0] != message.from_user.id, msg_to_be_watched))
        msg_to_be_watched.append((message.chat.id, []))
    else:
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


cmdhelp_instance.add_commands(["bahan", "material"], "Get materials")
