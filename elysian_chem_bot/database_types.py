from dataclasses import dataclass
from typing import Any


@dataclass
class SectionCheckStatus[T]:
    status: bool
    value: T | None = None


@dataclass
class File:
    file_id: str
    file_unique_id: str


type Sections = list[str]
type Section = dict | Any
