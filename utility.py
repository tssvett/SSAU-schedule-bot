import os
import datetime
from random import choice


def picture_choose():
    path = os.path.dirname(__file__) + '/pictures'.strip()
    file_name = choice(
        os.listdir(path))
    path += '/ '.strip() + file_name
    picture = open(path, 'rb')
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
