from dataclasses import dataclass
from typing import List


@dataclass
class Lesson:
    time: str
    title: List
    groups: List
    place: List
    teacher: List
    is_online: bool
    is_empty: bool
    url: str
