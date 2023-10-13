from utility import week_calc
from bs4 import BeautifulSoup
from requests import get
from DataClasses import Lesson, ScheduleDay


class Schedule:
    def __init__(self, day_number=0, group_id=799359428):
        self.group_id = group_id
        self.week = week_calc(day_number)
        self.week_url = self._get_url()
        self.is_alive = self.alive_check()
        self.soup = None

    def _get_url(self):
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

    def _parse_week(self, days, dates, times):
        resulted_week = []
        information = self.soup.find_all('div', 'schedule__item')
        del information[0:7]
        for i in range(6):
            day_name = days[i].capitalize()
            date = dates[i]
            lessons = []
            for j in range(i, len(information), 6):
                title = [f.text.strip().capitalize() for f in information[j].find_all('div', 'schedule__discipline')]
                time = self.get_time(title, j, times)
                place = [f.text.strip().capitalize() for f in information[j].find_all('div', 'schedule__place')]
                teacher = [f.text.strip() for f in information[j].find_all('div', 'schedule__teacher')]
                groups = [f.text.strip() for f in information[j].find_all('div', 'schedule__groups')]
                lessons.append(Lesson(time, title, groups, place, teacher, self._is_online(place),
                                      self._is_empty(title)))
            resulted_week.append(ScheduleDay(day_name, date, lessons,  self._is_empty(lessons)))
        return resulted_week

    @staticmethod
    def get_time(title, j, times):
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

    def get_week(self):
        response = get(self.week_url)
        if not response.ok:
            return None
        self.soup = BeautifulSoup(response.text, features="html.parser")
        times = self._parse_time()
        days, dates = self._parse_days()
        return self._parse_week(days, dates, times)

    def alive_check(self):
        response = get(self.week_url)
        return response.ok
