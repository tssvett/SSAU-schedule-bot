import aiogram
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import re
import asyncio



class Lecture:
    """
    Класс Лекции. Содержит в себе информацию о лекции включая:
    Название лекции, ссылку на нее, время лекции, название видио с этой лекцией.
    """

    def __init__(self, dictionary_name):
        self.name = dictionary_name
        self.dictonary = {"Тест ббб": "https://bbb.ssau.ru/b/ytv-16f-opd-thk",
                     "Тест Зума": "https://us04web.zoom.us/j/898107462"
                                  "5?pwd=AtPGRhBjeYf9HMbp77omA8rcFDesdI.1",
                     "Физика": "https://bbb.ssau.ru/b/qrq-nyv-h9n",
                     "ООП": "https://bbb.ssau.ru/b/h2q-g66-ppu",
                     "Диффуры": "https://bbb.ssau.ru/b/2d4-4jg-ypw",
                     "ИОТ": "https://bbb.ssau.ru/b/ytv-16f-opd-thk",
                     "Матан": "https://bbb.ssau.ru/b/9r9-ryk-fy9",
                     "Теорвер и матстат": "https://bbb.ssau.ru/b/em3-wnv-ph6",
                     "Алгебраические структуры": "https://bbb.ssau.ru/b/44k-gvk-44h-qgp",
                     "ИИ": "https://us06web.zoom.us/j/96499138958",
                     "Основы Языкознания": "https://bbb.ssau.ru/b/n3m-hp2-vun",
                     }
        self.url = self.dictonary[self.name]



class Autojoin:

    def __init__(self, telebot: aiogram.Bot):
        self.telebot = telebot
        self.message = None
        self.name = None
        self.lecture = None
        self.allowed = ["Тест ббб", "Тест Зума", "Физика","ООП", "Диффуры", "ИОТ", "Матан","Теорвер и матстат", "Алгебраические структуры","ИИ","Основы Языкознания"]
        self.listeners = None
        self.service, self.chrome_options = self.setup_driver()
        self.browser = webdriver.Chrome(service=self.service, options=self.chrome_options)


    def set_name(self, new_name):
        self.name = new_name

    def set_lecture(self, new_lecture):
        self.lecture = Lecture(new_lecture)

    def set_message(self, message):
        self.message = message

    def get_name(self):
        return self.name

    def get_lecture(self):
        return self.lecture


    def setup_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        service = ChromeService(executable_path='chromedriver.exe')
        return service, chrome_options

    def load_waiting(self, id):
        """
        Ожидание
        """
        while len(self.browser.find_elements(By.ID, id)) == 0:
            time.sleep(5)

    def parse_listeners(self) -> int:
        """
        Возвращает количество людей на лекции
        """
        xpath ='//*[@id="layout"]/div[1]/div/div/div[3]/div[1]/h2'
        while len(self.browser.find_elements(By.XPATH, xpath)) == 0:
            time.sleep(5)
        raw_listeners_number = self.browser.find_element(By.XPATH, xpath).text
        listeners_number = int(re.search(r'\d+', raw_listeners_number).group())
        self.listeners = listeners_number
        return listeners_number

    async def start_session(self):
        """
        Заход на лекцию_
        """
        await self.telebot.send_message(self.message.chat.id, f'Захожу под именем [{self.name}] на лекцию [{self.lecture.name}]')
        self.browser.get(url=self.lecture.url)
        await self.telebot.send_message(self.message.chat.id, f'Ввожу имя')
        self.name_input()
        await self.telebot.send_message(self.message.chat.id, f'Имя введено! Подключаюсь на лекцию...')
        self.join()
        await self.telebot.send_message(self.message.chat.id, f'Подключение пошло успешно! Выбираю только слушать')
        self.set_headphones_only()
        await self.telebot.send_message(self.message.chat.id, f'Все прошло отлично! Текущее число '
                                                                  f'людей на лекции: {self.parse_listeners()}')
        await self.telebot.send_message(self.message.chat.id, f'Пишу приветствие в чат')
        self.greeting_input()
        await self.telebot.send_message(self.message.chat.id, f'Написал. Отправляю')
        self.greeting_send()
        await self.check_status()
        await asyncio.sleep(95 * 60)

    async def end_session(self):
        """
        Выход с лекции
        """
        self.browser.close()
        self.browser.quit()
        await self.telebot.send_message(self.message.chat.id, f'Лекция [{self.lecture.name}] закончена или прервана. Очищаю сессию...')
        temp_message = self.message
        self.__init__(self.telebot)
        self.set_message(temp_message)

    async def check_status(self):
        try:
            current_info = f"✅✅✅Вы находитесь на лекции✅✅✅\n" \
                           f"Имя: {self.name}\n" \
                           f"Лекция: {self.lecture.name}\n" \
                           f"Количество людей на лекции: {self.listeners}"
            await self.telebot.send_message(self.message.chat.id, current_info)
        except:
            await self.telebot.send_message(self.message.chat.id, '❌❌❌АЛЯРМ БЛЯТЬ НЕТ СОЕДИНЕНИЯ С ЛЕКЦИЕЙ❌❌❌')


    def greeting_input(self):
        """
        Вводит приветствие в окно ввода чата
        """
        id = 'message-input'
        self.load_waiting(id)
        chat = self.browser.find_element(By.ID, id)
        chat.clear()
        time.sleep(1)
        chat.send_keys('Привет')

    def greeting_send(self):
        """
        Нажимаетие на кнопку "Отправить" в чат
        """
        id = 'tippy-20'
        self.load_waiting(id)
        chat_send_btn = self.browser.find_element(By.ID,id)
        time.sleep(1)
        chat_send_btn.click()

    def name_input(self):
        """
        Вводит имя в окно ввода
        """
        id = '_b_ytv-16f-opd-thk_join_name'
        self.load_waiting(id)
        textbox = self.browser.find_element(By.ID, id)
        textbox.clear()
        time.sleep(1)
        textbox.send_keys(self.name)

    def join(self):
        """
        Нажимает на кнопку "Присоединиться"
        """
        id = 'room-join'
        self.load_waiting(id)
        join = self.browser.find_element(By.ID, id)
        time.sleep(1)
        join.click()

    def set_headphones_only(self):
        """
        Выбирает наушники
        """
        class_name = "icon-bbb-listen"
        while len(self.browser.find_elements(By.CLASS_NAME, class_name)) == 0:
            time.sleep(5)
        no_micro = self.browser.find_element(By.CLASS_NAME, class_name)
        time.sleep(1)
        no_micro.click()

