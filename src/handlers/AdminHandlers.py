import os

import aiogram
from aiogram.types import FSInputFile
from aiogram.filters import Command
from src.BotFile import dp, telebot
from src.MessagesFile import NOT_ADMIN_MESSAGE, ADMIN_MESSAGE, HELP_ADMIN_MESSAGE, NEW_PICTURE_MESSAGE, ALREADY_EXIST_PICTURE_MESSAGE
from src.AdminPanelClass import admin_panel


@dp.message(Command('amount'))
async def choose_schedule(message: aiogram.types.Message):
    if message.from_user.id == admin_panel.get_admin_id():
        await message.answer(ADMIN_MESSAGE + '\n\n' + "☘️ Текущее количество пользователей:"
                                                      " " + str(admin_panel.get_users_number()))
    else:
        await message.answer(NOT_ADMIN_MESSAGE)


@dp.message(Command('admin'))
async def admin_message(message: aiogram.types.Message):
    if message.from_user.id == admin_panel.get_admin_id():
        await message.answer(HELP_ADMIN_MESSAGE)
    else:
        await message.answer(NOT_ADMIN_MESSAGE)


@dp.message(lambda message: message.photo)
async def send_picture(message: aiogram.types.Message):
    if message.from_user.id != admin_panel.get_admin_id():
        await message.answer(NOT_ADMIN_MESSAGE)
    else:
        file = await telebot.get_file(message.photo[-1].file_id)
        tg_server_file_path = file.file_path
        new_picture_name = tg_server_file_path.split('photos/')[1]
        new_picture_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r"/pictures/[" + new_picture_name
        if os.path.exists(new_picture_path):
            await message.answer(ALREADY_EXIST_PICTURE_MESSAGE)
        else:
            print(new_picture_path)
            await telebot.download_file(tg_server_file_path, new_picture_path)
            await telebot.send_photo(chat_id=message.chat.id, photo=FSInputFile(new_picture_path), caption=NEW_PICTURE_MESSAGE)

