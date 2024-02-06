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
        file_name = choice(listdir(dirname(dirname(__file__)) + r'/pictures'))
    path = dirname(dirname(__file__)) + f'/pictures/{file_name}'
    picture = FSInputFile(path, filename=file_name)
    return picture


def day_calc(day_number=0) -> int:
    start_day = datetime.datetime(2024, 2, 5).date()
    now = datetime.datetime.now().date()
    now += datetime.timedelta(days=day_number)
    difference = (now - start_day).days
    day = (difference % 7)
    print("day = " + str(day))
    return day


def week_calc(day_number=0) -> int:
    current_day = datetime.datetime.now() + datetime.timedelta(days=day_number)
    print("Сегодня: " + str(current_day))
    lasted_weeks = 23
    week = current_day.isocalendar()[1] - datetime.datetime(2024, 2, 5).isocalendar()[1] + 1 + lasted_weeks
    print("HUINYA:" + str(current_day.isocalendar()[1]))
    print("week = " + str(week))
    return week
