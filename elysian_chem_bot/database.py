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

import atexit
import json
import logging
from pathlib import Path
from typing import Any, cast

from elysian_chem_bot.database_types import File, Section, SectionCheckStatus, Sections

log: logging.Logger = logging.getLogger(__name__)


class Database:
    """Currently using JSON."""

    def __init__(self, db_path: str = "") -> None:  # noqa: D107
        self.db_path = db_path
        self.db_loaded: bool = False
        self.raw_db: dict[str, Any] | None = None

        self.load_db()
        atexit.register(self._atexit)

    def load_db(self) -> None:  # noqa: D102
        with Path(self.db_path).open(encoding="utf-8") as f:
            self.raw_db = json.load(f)
            if not isinstance(self.raw_db, dict):
                msg = f"something is wrong with database, the type is: {type(self.raw_db)}"
                raise TypeError(msg)

    def write_db(self) -> None:  # noqa: D102
        with Path(self.db_path).open("w", encoding="utf-8") as f:
            json.dump(self.raw_db, f)

    def is_sections_exist(self, sections: Sections) -> SectionCheckStatus:
        """Determines if the sections exist in the database.

        Args:
            sections (list[str]): The sections to check.

        Returns:
            SectionCheckStatus: which has two fields: status and value,
                where value is the section that does not exist.

        """
        cur_section: Section = self.raw_db
        for sec in sections:
            cur_section = cur_section.get(sec)
            if cur_section is None or not isinstance(cur_section, dict):
                return SectionCheckStatus(status=False, value=cur_section)

        return SectionCheckStatus(status=True, value=None)

    def add_section(self, sections: Sections) -> None:
        """Adds a section to the database.

        Args:
            sections (list[str]): The sections to add.

        """
        cur_section: Section = self.raw_db
        for sec in sections:
            cur_section = cur_section.setdefault(sec, {})

    def remove_section(self, sections: Sections) -> None:
        """Removes a section from the database. Only the last element in the sections list will be removed.

           The rest serves as the path to the section.

        Args:
            sections (list[str]): The section to be removed must be the last element.

        Returns:
            None

        """
        cur_section: Section = self.raw_db
        for sec in sections[:-1]:
            cur_section = cur_section.get(sec)
            if cur_section is None:
                return

        cur_section.pop(sections[-1])

    def add_file(self, sections: Sections, file_name: str, file_id: str, file_unique_id: str) -> None:  # noqa: D102
        status = self.is_sections_exist(sections).status
        if not status:
            msg = "sections does not exist!"
            raise ValueError(msg)

        cur_section: Section = self.raw_db
        for sec in sections:
            cur_section = cur_section.get(sec)

        cur_section[file_name] = (file_id, file_unique_id)

    def remove_file(self, sections: Sections, file_name: str) -> None:  # noqa: D102
        status = self.is_sections_exist(sections).status
        if not status:
            msg = "sections does not exist!"
            raise ValueError(msg)

        cur_section: Section = self.raw_db
        for sec in sections:
            cur_section = cur_section.get(sec)

        cur_section.pop(file_name)

    def get_file(self, sections: Sections, file_name: str) -> File:  # noqa: D102
        status = self.is_sections_exist(sections).status
        if not status:
            msg = "sections does not exist!"
            raise ValueError(msg)

        cur_section: Section = self.raw_db
        for sec in sections:
            cur_section = cur_section.get(sec)

        file_id, file_unique_id = cast(dict, cur_section.get(file_name))
        if file_id is None:
            msg = "file does not exist!"
            raise ValueError(msg)

        return File(file_id, file_unique_id)

    def list_files(self, sections: Sections) -> list[str]:  # noqa: D102
        status = self.is_sections_exist(sections).status
        if not status:
            msg = "sections does not exist!"
            raise ValueError(msg)

        cur_section: Section = self.raw_db
        for sec in sections:
            cur_section = cur_section.get(sec)

        return list(cur_section.keys())

    def _atexit(self) -> None:
        log.info("atexit trigger: saving db to file")
        self.write_db()
