import aiogram
from aiogram.filters import Command
from src.BotFile import dp
from src.MessagesFile import NOT_ADMIN_MESSAGE, ADMIN_MESSAGE, HELP_ADMIN_MESSAGE
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
