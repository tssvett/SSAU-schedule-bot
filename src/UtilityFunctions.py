from aiogram.types import FSInputFile
from os import listdir
from os.path import dirname
import datetime
from random import choice


def picture_choose(file_name: str = None) -> FSInputFile:
    """
    Create FSInputFile instance from random photo in pictures directory
    :param file_name:
    :return: random or selected FSInputFile photo
    """
    if file_name is None:
        file_name = choice(listdir(dirname(dirname(__file__)) + r'\pictures'))
        print(file_name)
    path = dirname(dirname(__file__)) + f'\pictures\{file_name}'
    picture = FSInputFile(path, filename=file_name)
    return picture


def day_calc(day_number=0) -> int:
    start_day = datetime.datetime(2023, 8, 21).date()
    now = datetime.datetime.now().date()
    now += datetime.timedelta(days=day_number)
    difference = (now - start_day).days
    day = (difference % 7)
    return day


def week_calc(day_number=0) -> int:
    current_day = datetime.datetime.now() + datetime.timedelta(days=day_number)
    return current_day.isocalendar()[1] - datetime.datetime(2023, 9, 1).isocalendar()[1] + 1
