import os

import aiogram
from aiogram.types import FSInputFile
from aiogram.filters import Command
from src.BotFile import dp, telebot
from src.MessagesFile import ADMIN_MESSAGE, HELP_ADMIN_MESSAGE, NEW_PICTURE_MESSAGE, \
    ALREADY_EXIST_PICTURE_MESSAGE
from src.AdminPanelClass import admin_panel
from src.Filters.AdminFilter import AdminFilter
from src.ScheduleClass import Schedule
from src.OutputClass import CustomOutput
from src.UtilityFunctions import day_calc


@dp.message(Command('amount'), AdminFilter())
async def choose_schedule(message: aiogram.types.Message):
    await message.answer(ADMIN_MESSAGE + '\n\n' + "☘️ Текущее количество пользователей:"
                                                  " " + str(admin_panel.get_users_number()))


@dp.message(Command('admin'), AdminFilter())
async def admin_message(message: aiogram.types.Message):
    await message.answer(HELP_ADMIN_MESSAGE)


@dp.message(Command('rasp'), AdminFilter())
async def admin_message(message: aiogram.types.Message):
    schedule = Schedule(message.from_user.id, day_difference=0)
    print(schedule.week_url)
    week = schedule.get_week()
    print(week)
    #await message.answer(schedule.get_week(), parse_mode='html')


@dp.message(lambda message: message.photo, AdminFilter())
async def send_picture(message: aiogram.types.Message):
    file = await telebot.get_file(message.photo[-1].file_id)
    tg_server_file_path = file.file_path
    new_picture_name = tg_server_file_path.split('photos/')[1]
    new_picture_path = os.path.dirname(
        os.path.dirname(os.path.dirname(__file__))) + r"/pictures/[" + new_picture_name
    if os.path.exists(new_picture_path):
        await message.answer(ALREADY_EXIST_PICTURE_MESSAGE)
    else:
        print(new_picture_path)
        await telebot.download_file(tg_server_file_path, new_picture_path)
        await telebot.send_photo(chat_id=message.chat.id, photo=FSInputFile(new_picture_path),
                                 caption=NEW_PICTURE_MESSAGE)
