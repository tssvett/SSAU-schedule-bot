import aiogram
from aiogram.types import ParseMode
from config import TOKEN


telebot = aiogram.Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = aiogram.Dispatcher(telebot)
