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

from typing import Union, Iterable

from elysian_chem_bot import app


async def sanitize_message(text: str, command: Union[Iterable[str], str]) -> str:
    """cleans /command or /command@username from the incoming message."""
    username = (await app.get_me()).username

    if isinstance(command, str):
        command = [command]

    for cmd in command:
        text = text.removeprefix(f"/{cmd}")

    text = text.removeprefix(f"@{username}")
    return text.strip()
