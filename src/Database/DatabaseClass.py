import pathlib
import sqlite3
import sys
from config import facilities


class Database:
    def __init__(self):
        self.path = pathlib.Path(sys.argv[0]).parent /'src'/'Database' / 'database.db'
        print(self.path)
        self.connection = sqlite3.connect(self.path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def is_registered(self, user_id):
        self.cursor.execute('SELECT * FROM BotInformation WHERE user_id = ? AND current_state = "REGISTERED"', (user_id,))
        if self.cursor.fetchone() is None:
            return False
        return True

    def add_new_user(self, user_id: int, faculty_id: str, group_id: str, current_state: str, course_id: str):
        """
        Add new user to database
        :param user_id:
        :param faculty_id:
        :param group_id:
        :param current_state:
        :param course_id:
        :return:
        """
        self.cursor.execute('INSERT INTO BotInformation (user_id, faculty_id, group_id, current_state, course_id) VALUES (?, ?, ?, ?, ?)', (user_id, faculty_id, group_id, current_state, course_id))
        self.connection.commit()

    def update_faculty(self, user_id, faculty: str):
        """
        Update faculty in database
        :param user_id:
        :param faculty_id:
        :return:
        """
        faculty_id = facilities.get(faculty)
        self.cursor.execute('UPDATE BotInformation SET faculty_id = ? WHERE user_id = ?', (faculty_id, user_id))
        self.connection.commit()

    def update_course(self, user_id, course_id: str):
        """
        Update course in database
        :param user_id:
        :param course_id:
        :return:
        """
        self.cursor.execute('UPDATE BotInformation SET course_id = ? WHERE user_id = ?', (course_id, user_id))
        self.connection.commit()

    def update_group(self, user_id, group: str, groups: dict):
        """
        Update group in database
        :param user_id:
        :param group_id:
        :return:
        """
        self.cursor.execute('UPDATE BotInformation SET group_id = ? WHERE user_id = ?', (groups.get(group), user_id))
        self.connection.commit()

    def update_state(self, user_id, current_state: str):
        """
        Update state in database
        :param user_id:
        :param current_state:
        :return:
        """
        self.cursor.execute('UPDATE BotInformation SET current_state = ? WHERE user_id = ?', (current_state, user_id))
        self.connection.commit()

    def get_group(self, user_id):
        self.cursor.execute('SELECT group_id FROM BotInformation WHERE user_id = ?', (user_id,))
        group_id = self.cursor.fetchone()
        return group_id[0]

    def get_faculty(self, user_id):
        self.cursor.execute('SELECT faculty_id FROM BotInformation WHERE user_id = ?', (user_id,))
        faculty_id = self.cursor.fetchone()
        return faculty_id[0]

    def get_state(self, user_id):
        self.cursor.execute('SELECT current_state FROM BotInformation WHERE user_id = ?', (user_id,))
        state = self.cursor.fetchone()
        return state[0]

    def get_course(self, user_id):
        self.cursor.execute('SELECT course_id FROM BotInformation WHERE user_id = ?', (user_id,))
        course_id = self.cursor.fetchone()
        return course_id[0]

    def get_users_amount(self) -> int:
        self.cursor.execute('SELECT user_id FROM BotInformation')
        users_list = self.cursor.fetchall()
        return len(users_list)


db = Database()
