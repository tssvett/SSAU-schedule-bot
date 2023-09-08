from config import BBB


class CustomOutput:
    def __init__(self, week_to_customize):
        self.week = week_to_customize
        self.bbb_urls = BBB

    def raw(self):
        for day in self.week:
            print(day)
            print()

    def day(self, day_number: int):
        if day_number > 5:
            return 'Воскресенье зачилься'
        current_day = self.week[day_number]
        header = ''
        body = ''
        if 0 <= day_number <= 5:
            header += '<b>' + current_day.name + ' ' + current_day.date + '</b>' + '\n'
            for lesson in current_day.lessons:
                if not lesson.is_empty:
                    body += '<i>' + lesson.time + '</i>' + '  ' + lesson.title[0] + '\n'
                    if len(lesson.groups) > 1:
                        body += '\n'
                        for subgroup in range(len(lesson.teacher)):
                            body += self.get_subgroup(lesson.groups[subgroup]) + ' ' + lesson.teacher[subgroup] + ' ' \
                                    + self.add_url_to_title(lesson.place[subgroup], lesson.title[subgroup]) + '\n\n'
                    else:
                        body += lesson.teacher[0] + ' ' + self.add_url_to_title(lesson.place[0], lesson.title[0]) + '\n\n'
            if not body:
                body += "Пар нет, отдыхам реbyata" + '\n'
            return header + body + '\n'
        else:
            print("ты долбаеб?")

    def weeke(self):
        """
        Части сделал только ради возможного деления недели пополам
        """
        part1 = ''
        part2 = ''
        for i in range(3):
            part1 += self.day(i)
        for i in range(3, 6):
            part2 += self.day(i)
        return part1, part2

    @staticmethod
    def get_subgroup(group):  # Функция фильтрует группу от подгрупп и берет только подгруппы
        if group == '':
            return group
        if group[0] == '6':
            tmp = ''
            return tmp
        return group

    def add_url_to_title(self, place, discipline):
        if place[0] == "O":
            place = '🟢 '
            place += '<b>' + f'<a href="{self.bbb_urls[discipline]}">Подключиться</a>' + '</b>'
        else:
            place = '<b>' + '<i>' + place + '</i>' + '</b>' + ' 🔴 '
        return place
