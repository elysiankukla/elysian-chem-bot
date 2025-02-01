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

import json
from typing import Any, cast


class Database:
    """Currently using JSON."""

    def __init__(self, db_path: str = "") -> None:
        self.db_path = db_path
        self.db_loaded: bool = False
        self.raw_db: dict | None = None

        self.load_db()

    def load_db(self) -> None:
        with open(self.db_path, "r", encoding="utf-8") as f:
            self.raw_db = json.load(f)
            if isinstance(self.raw_db, dict):
                raise TypeError(f"something is wrong with database, the type is: {type(self.raw_db)}")

    def write_db(self) -> None:
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.raw_db, f)

    def is_sections_exist(self, sections: list[str]) -> tuple[bool, str | None]:
        """Determines if the sections exist in the database.

        Args:
            sections (list[str]): The sections to check.

        Returns:
            tuple[bool, str | None]: A tuple containing a boolean and a string,
                where the boolean is True if the sections exist,
                and the string is the section that does not exist.
        """
        cur_section: dict | Any = self.raw_db
        for sec in sections:
            cur_section = cur_section.get(sec)
            if cur_section is None:
                return False, cur_section

        return True, None

    def add_section(self, sections: list[str]) -> None:
        """Adds a section to the database.

        Args:
            sections (list[str]): The sections to add.
        """
        cur_section: dict | Any = self.raw_db
        for sec in sections:
            cur_section = cur_section.setdefault(sec, {})

    def remove_section(self, sections: list[str]) -> None:
        """Removes a section from the database. Only the last element in the sections list will be removed.
           The rest serves as the path to the section.

        Args:
            sections (list[str]): The section to be removed must be the last element.

        Returns:
            None
        """
        cur_section: dict | Any = self.raw_db
        for sec in sections[:-1]:
            cur_section = cur_section.get(sec)
            if cur_section is None:
                return

        cur_section.pop(sections[-1])

    def add_file(self, sections: list[str], file_name: str, file_id: str, file_unique_id: str) -> None:
        _, status = self.is_sections_exist(sections)
        if not status:
            raise ValueError("sections does not exist!")

        cur_section: dict | Any = self.raw_db
        for sec in sections:
            cur_section = cur_section.get(sec)

        cur_section[file_name] = (file_id, file_unique_id)

    def remove_file(self, sections: list[str], file_name: str) -> None:
        _, status = self.is_sections_exist(sections)
        if not status:
            raise ValueError("sections does not exist!")

        cur_section: dict | Any = self.raw_db
        for sec in sections:
            cur_section = cur_section.get(sec)

        cur_section.pop(file_name)

    def get_file(self, sections: list[str], file_name: str) -> tuple[str, str]:
        _, status = self.is_sections_exist(sections)
        if not status:
            raise ValueError("sections does not exist!")

        cur_section: dict | Any = self.raw_db
        for sec in sections:
            cur_section = cur_section.get(sec)

        file_id, file_unique_id = cast(dict, cur_section.get(file_name))
        if file_id is None:
            raise ValueError("file does not exist!")

        return file_id, file_unique_id

    def list_files(self, sections: list[str]) -> list[str]:
        _, status = self.is_sections_exist(sections)
        if not status:
            raise ValueError("sections does not exist!")

        cur_section: dict | Any = self.raw_db
        for sec in sections:
            cur_section = cur_section.get(sec)

        return list(cur_section.keys())
