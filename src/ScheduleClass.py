import re
from UtilityFunctions import week_calc
from bs4 import BeautifulSoup
from requests import get
from src.DataClasses.DayClass import Lesson, Day
from src.LoggerClass import Logger
from src.Database.DatabaseClass import db



class Schedule:
    """
    Schedule class for parsing schedule from SSAU website.
    """
    def __init__(self, user_id,  day_difference=0,):
        """

        :param day_difference: user for output schedule for different days (difference between today and variable day)
        :param group_id: used for output schedule for different groups
        """
        self.logger = Logger('Schedule')
        self.group_id = db.get_group(user_id)
        self.week = week_calc(day_difference)
        self.week_url = self._get_url()
        self.is_alive = self.alive_check()
        self.soup = None

    def _get_url(self):
        """
        Get url for parsing schedule for different groups
        :return:
        """
        self.week_url = f'https://ssau.ru/rasp?groupId={self.group_id}&selectedWeek={self.week}'
        return self.week_url

    def _parse_time(self):
        time_list = []
        times = self.soup.find_all('div', 'schedule__time')
        for i in range(len(times)):
            time = times[i].text.strip()
            arr = time.split(' ')
            arr[1] = ' - '
            time_list.append(' '.join(arr))
        return time_list

    def _parse_days(self):
        day_list = []
        date_list = []
        days = self.soup.find_all('div', 'schedule__item schedule__head')
        del days[0]
        for i in range(len(days)):
            day = days[i].text.strip()
            arr = day.split(' ')
            day_list.append(arr[0])
            date_list.append(arr[1])
        return day_list, date_list

    def _parse_week(self, days, dates, times) -> list[Day]:
        resulted_week = []
        information = self.soup.find_all('div', 'schedule__item')
        del information[0:7]
        for i in range(6):
            day_name = days[i].capitalize()
            date = dates[i]
            lessons = []
            for j in range(i, len(information), 6):
                title = [f.text.strip().capitalize() for f in information[j].find_all('div', 'schedule__discipline')]
                time = self._get_time(title, j, times)
                place = [f.text.strip().capitalize() for f in information[j].find_all('div', 'schedule__place')]
                teacher = [f.text.strip() for f in information[j].find_all('div', 'schedule__teacher')]
                groups = [f.text.strip() for f in information[j].find_all('div', 'schedule__groups')]
                lessons.append(Lesson(time, title, groups, place, teacher, self._is_online(place),
                                      self._is_empty(title)))
            resulted_week.append(Day(day_name, date, lessons, self._is_empty(lessons)))
        return resulted_week

    @staticmethod
    def _get_time(title, j, times):
        if not title:
            time = ''
        else:
            time = times[j // 6]
        return time

    @staticmethod
    def _is_empty(lessons):
        for lesson in lessons:
            if lesson.title:
                return False
        return True

    @staticmethod
    def _is_online(place):
        if not place:
            return False
        elif place[0] == "O":
            return True
        else:
            return False

    def get_week(self) -> list[Day] | None:
        """
        Return raw parsed schedule
        :return: list(list)
        """
        response = get(self.week_url)
        if not response.ok:
            self.logger.send_message('SSAU is down', 'info')
            return None
        self.soup = BeautifulSoup(response.text, features="html.parser")
        times = self._parse_time()
        days, dates = self._parse_days()
        return self._parse_week(days, dates, times)

    def alive_check(self):
        response = get(self.week_url)
        return response.ok

    def get_faculties(self):
        response = get('https://ssau.ru/rasp')
        page = response.text
        soup = BeautifulSoup(page, features='html.parser')
        return {item.a.text.strip(): int(re.search(r'\d+', item.a.attrs['href']).group())
                for item in soup.find_all('div', class_='faculties__item')}

    @staticmethod
    def get_groups(faculty: int, course: int):
        response = get(f'https://ssau.ru/rasp/faculty/{faculty}?course={course}')
        page = response.text
        soup = BeautifulSoup(page, features='html.parser')
        return {item.text.strip(): int(re.search(r'\d+', item.attrs['href']).group())
                for item in soup.find_all('a', class_='group-catalog__group')}
