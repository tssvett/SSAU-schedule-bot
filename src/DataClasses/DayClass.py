from dataclasses import dataclass
from typing import List
from src.DataClasses.LessonClass import Lesson


@dataclass
class Day:
    name: str
    date: str
    lessons: List[Lesson]
    is_empty: bool
