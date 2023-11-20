import aiogram
from aiogram.filters import CommandStart, Command
from src.BotFile import dp, telebot
from src.ButtonsFile import schedule_buttons
from src.OutputClass import CustomOutput
from src.UtilityFunctions import picture_choose, day_calc
from src.ScheduleClass import Schedule
from src.MessagesFile import DEAD_MESSAGE, GREETING_MESSAGE, HELP_MESSAGE
from config import polina_id


def group_choose(day, message):
    if message.from_user.id == polina_id:
        schedule = Schedule(day_difference=day, group_id=701780995)
    else:
        schedule = Schedule(day_difference=day, group_id=799359428)
    return schedule


@dp.message(CommandStart())
async def starting(message: aiogram.types.Message):
    picture = picture_choose("Lain.jpg")
    await telebot.send_photo(message.chat.id, picture, caption=GREETING_MESSAGE)


@dp.message(Command('help'))
async def choose_schedule(message: aiogram.types.Message):
    await message.answer(HELP_MESSAGE, reply_markup=schedule_buttons)


@dp.message(lambda message: message.text.lower() == 'сегодня')
async def today_schedule(message: aiogram.types.Message):
    schedule = group_choose(0, message)
    picture = picture_choose()
    if schedule.is_alive:
        out = CustomOutput(schedule.get_week())
        await telebot.send_photo(message.chat.id, picture, caption=out.day(day_calc()), parse_mode='html')
    else:
        await telebot.send_photo(message.chat.id, picture, caption=DEAD_MESSAGE)


@dp.message(lambda message: message.text.lower() == 'завтра')
async def tomorrow_schedule(message: aiogram.types.Message):
    schedule = group_choose(1, message)
    picture = picture_choose()
    if schedule.is_alive:
        out = CustomOutput(schedule.get_week())
        await telebot.send_photo(message.chat.id, picture, caption=out.day(day_calc(1)), parse_mode='html')
    else:
        await telebot.send_photo(message.chat.id, picture, caption=DEAD_MESSAGE)


@dp.message(lambda message: message.text.lower() == 'послезавтра')
async def double_tomorrow_schedule(message: aiogram.types.Message):
    schedule = group_choose(2, message)
    picture = picture_choose()
    if schedule.is_alive:
        out = CustomOutput(schedule.get_week())

        await telebot.send_photo(message.chat.id, picture, caption=out.day(day_calc(2)), parse_mode='html')
    else:
        await telebot.send_photo(message.chat.id, picture, caption=DEAD_MESSAGE)


@dp.message(lambda message: message.text.lower() == 'текущая неделя' or message.text.lower() == 'текущая')
async def current_week_schedule(message: aiogram.types.Message):
    schedule = group_choose(0, message)
    picture = picture_choose()
    if schedule.is_alive:
        out = CustomOutput(schedule.get_week())
        part1, part2 = out.weeke()
        await telebot.send_message(message.chat.id, part1 + part2, disable_web_page_preview=True)
    else:
        await telebot.send_photo(message.chat.id, picture, caption=DEAD_MESSAGE)


@dp.message(lambda message: message.text.lower() == 'следующая неделя' or message.text.lower() == 'следующая')
async def next_week_schedule(message: aiogram.types.Message):
    schedule = group_choose(7, message)
    picture = picture_choose()
    if schedule.is_alive:
        out = CustomOutput(schedule.get_week())
        part1, part2 = out.weeke()
        await telebot.send_message(message.chat.id, part1 + part2, disable_web_page_preview=True)
    else:
        await telebot.send_photo(message.chat.id, picture, caption=DEAD_MESSAGE)


@dp.message(lambda message: message.text.lower() == 'пикрандом')
async def pic_random(message: aiogram.types.Message):
    await telebot.send_photo(message.chat.id, picture_choose())
