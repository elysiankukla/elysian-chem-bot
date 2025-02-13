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

import asyncio
import time

from pyrogram.client import Client
from pyrogram.filters import command
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types.messages_and_media import Message

from elysian_chem_bot import SUPER_USERS, app, cmdhelp_instance


async def start(client: Client, message: Message) -> None:
    await message.reply_text("Send /bahan to get started!")


async def reload_modules(client: Client, message: Message) -> None:
    if message.from_user.id not in SUPER_USERS:
        return

    msg = await message.reply_text("Reloading plugins...")
    start = time.perf_counter()
    app.load_plugins()
    stop = time.perf_counter()
    await msg.edit_text(f"**Plugins reloaded.** Took {stop - start} seconds")


def main() -> None:
    app.add_handler(MessageHandler(start, command("start")))
    app.add_handler(MessageHandler(reload_modules, command("reload")))

    cmdhelp_instance.add_commands("start", "start the bot")
    app.load_plugins()
    _ = app.start()
    cmdhelp_instance.update_commands_telegram()

    asyncio.get_event_loop().run_forever()
