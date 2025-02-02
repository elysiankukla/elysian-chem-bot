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

import os
import inspect

from pathlib import Path

from pyrogram.client import Client

API_ID: int = int(os.getenv("API_ID", 0))
API_HASH: str = os.getenv("API_HASH", "")
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
MODULE_DIR: str = str(Path(inspect.getfile(lambda _: _)).parent)

if any((API_ID == 0, API_HASH == "", BOT_TOKEN == "")):
    raise ValueError("please set API_ID, API_HASH and BOT_TOKEN properly")

plugins: dict[str, str] = {"root": f"{__name__.removesuffix('.main')}.plugins"}
app: Client = Client("elysian_chem_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins=plugins)
