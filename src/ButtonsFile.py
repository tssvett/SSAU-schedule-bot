from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


today = KeyboardButton(text='Сегодня')
tomorrow = KeyboardButton(text='Завтра')
current_week = KeyboardButton(text='Текущая неделя')
next_week = KeyboardButton(text='Следующая неделя')
keyboard = [[tomorrow, next_week, today, current_week]]
schedule_buttons = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
