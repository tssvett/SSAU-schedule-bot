import aiogram
import os
from bot import dp, telebot
from buttons import schedule_buttons
from utility import picture_choose, day_calc
from Schedule import Schedule
from CustomOutput import CustomOutput
from config import DEAD_MESSAGE


@dp.message_handler(commands=['start'])
async def starting(message: aiogram.types.Message):
    path = os.path.dirname(__file__) + '/pictures'.strip()
    file_name = "Lain.jpg"
    path += '/ '.strip() + file_name
    lain = open(path, 'rb')
    introduce = (
        f"Привет, {message.from_user.full_name}! Я - Лейн.\nЯ программа для вывода расписания Самарского "
        f"Университета для группы 6201-010302D.\nИспользуйте команду /help для дальнейшего пользования")
    await telebot.send_photo(message.chat.id, lain, caption=introduce)


@dp.message_handler(commands=['help'])
async def choose_schedule(message: aiogram.types.Message):
    await message.answer('Поддержка команд: \nСегодня, завтра, послезавтра, текущая неделя,'
                         ' следующая неделя, пикрандом',
                         reply_markup=schedule_buttons)


@dp.message_handler(lambda message: message.text.lower() == 'сегодня')
async def today_schedule(message: aiogram.types.Message):
    schedule = Schedule()
    picture = picture_choose()
    if schedule.is_alive:
        out = CustomOutput(schedule.get_week())
        await telebot.send_photo(message.chat.id, picture, caption=out.day(day_calc()), parse_mode='html')
    else:
        await telebot.send_photo(message.chat.id, picture, caption=DEAD_MESSAGE)


@dp.message_handler(lambda message: message.text.lower() == 'завтра')
async def tomorrow_schedule(message: aiogram.types.Message):
    schedule = Schedule(1)
    picture = picture_choose()
    if schedule.is_alive:
        out = CustomOutput(schedule.get_week())
        await telebot.send_photo(message.chat.id, picture, caption=out.day(day_calc(1)), parse_mode='html')
    else:
        await telebot.send_photo(message.chat.id, picture, caption=DEAD_MESSAGE)


@dp.message_handler(lambda message: message.text.lower() == 'послезавтра')
async def double_tomorrow_schedule(message: aiogram.types.Message):
    schedule = Schedule(2)
    picture = picture_choose()
    if schedule.is_alive:
        out = CustomOutput(schedule.get_week())
        await telebot.send_photo(message.chat.id, picture, caption=out.day(day_calc(2)), parse_mode='html')
    else:
        await telebot.send_photo(message.chat.id, picture, caption=DEAD_MESSAGE)


@dp.message_handler(lambda message: message.text.lower() == 'текущая неделя')
async def current_week_schedule(message: aiogram.types.Message):
    schedule = Schedule(0)
    picture = picture_choose()
    if schedule.is_alive:
        out = CustomOutput(schedule.get_week())
        part1, part2 = out.weeke()
        await telebot.send_message(message.chat.id, part1 + part2, disable_web_page_preview=True)
    else:
        await telebot.send_photo(message.chat.id, picture, caption=DEAD_MESSAGE)


@dp.message_handler(lambda message: message.text.lower() == 'следующая неделя')
async def next_week_schedule(message: aiogram.types.Message):
    schedule = Schedule(7)
    picture = picture_choose()
    if schedule.is_alive:
        out = CustomOutput(schedule.get_week())
        part1, part2 = out.weeke()
        await telebot.send_message(message.chat.id, part1+part2, disable_web_page_preview=True)
    else:
        await telebot.send_photo(message.chat.id, picture, caption=DEAD_MESSAGE)


@dp.message_handler(lambda message: message.text.lower() == 'пикрандом')
async def pic_random(message: aiogram.types.Message):
    await telebot.send_photo(message.chat.id, picture_choose())

