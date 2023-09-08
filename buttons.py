from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


today = KeyboardButton('Сегодня')
tomorrow = KeyboardButton('Завтра')
current_week = KeyboardButton('Текущая неделя')
next_week = KeyboardButton('Следующая неделя')
schedule_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
schedule_buttons.add(tomorrow, next_week, today, current_week)
