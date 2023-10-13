import aiogram
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN
from Autojoin import Autojoin


telebot = aiogram.Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = aiogram.Dispatcher(telebot, storage=MemoryStorage())
autojoin = Autojoin(telebot)
