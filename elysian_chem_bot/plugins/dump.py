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

import io
import json

from tempfile import NamedTemporaryFile

from elysian_chem_bot import db_instance

from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram.filters import command


@Client.on_message(command("dumpdb"))
async def dump_db(client: Client, message: Message) -> None:
    with NamedTemporaryFile(suffix=".json") as f:
        with open(f.name, "w", encoding="utf-8") as jf:
            json.dump(db_instance.raw_db, jf, indent=4)

        with open(f.name, "rb") as rf:
            await message.reply_document(rf)
