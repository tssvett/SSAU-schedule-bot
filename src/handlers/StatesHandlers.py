import aiogram.types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from src.BotFile import dp
from src.MessagesFile import START_REGISTER_MESSAGE, INCORRECT_FACULTY_MESSAGE, CORRECT_FACULTY_MESSAGE,\
    INCORRECT_COURSE_MESSAGE, CORRECT_COURSE_MESSAGE, INCORRECT_GROUP_MESSAGE, CORRECT_GROUP_MESSAGE,\
    SUCCESS_REGISTER_MESSAGE, ALREADY_REGISTERED_MESSAGE, REPEAT_REGISTER_MESSAGE
from src.Database.DatabaseClass import db
from src.ScheduleClass import Schedule
from config import facilities



class RegistrationForm(StatesGroup):
    FACULTY_WAITING = State()
    COURSE_WAITING = State()
    GROUP_WAITING = State()
    REGISTERED = State()


def is_correct_faculty(message: aiogram.types.Message):
    return message.text in facilities.keys()


def is_correct_group(message: aiogram.types.Message, groups):
    return message.text in groups


def is_correct_course(message: aiogram.types.Message):
    return message.text in ['1', '2', '3', '4', '5']


@dp.message(Command('repeat'))
async def change_state(message: aiogram.types.Message, state: FSMContext):
    await message.answer(REPEAT_REGISTER_MESSAGE)
    await state.set_state(RegistrationForm.FACULTY_WAITING)
    db.update_state(message.from_user.id, 'FACULTY_WAITING')


@dp.message(Command('register'))
async def start_state(message: aiogram.types.Message, state: FSMContext):
    if not db.is_registered(message.from_user.id):
        await message.answer(START_REGISTER_MESSAGE)
        await state.set_state(RegistrationForm.FACULTY_WAITING)
        db.add_new_user(message.from_user.id, None, None, None, None)
        db.update_state(message.from_user.id, 'FACULTY_WAITING')
    else:
        await message.answer(ALREADY_REGISTERED_MESSAGE)


@dp.message(RegistrationForm.FACULTY_WAITING)
async def faculty_choose(message: aiogram.types.Message, state: FSMContext):
    if not is_correct_faculty(message):
        await message.answer(INCORRECT_FACULTY_MESSAGE)
        await state.set_state(RegistrationForm.FACULTY_WAITING)
        db.update_state(message.from_user.id, 'FACULTY_WAITING')
    else:
        await message.answer(CORRECT_FACULTY_MESSAGE)
        await state.set_state(RegistrationForm.COURSE_WAITING)
        db.update_faculty(message.from_user.id, message.text)
        db.update_state(message.from_user.id, 'COURSE_WAITING')


@dp.message(RegistrationForm.COURSE_WAITING)
async def faculty_choose(message: aiogram.types.Message, state: FSMContext):
    if not is_correct_course(message):
        await message.answer(INCORRECT_COURSE_MESSAGE)
        await state.set_state(RegistrationForm.COURSE_WAITING)
        db.update_state(message.from_user.id, 'COURSE_WAITING')
    else:
        await message.answer(CORRECT_COURSE_MESSAGE)
        await state.set_state(RegistrationForm.GROUP_WAITING)
        db.update_course(message.from_user.id, message.text)
        db.update_state(message.from_user.id, 'GROUP_WAITING')


@dp.message(RegistrationForm.GROUP_WAITING)
async def group_choose(message: aiogram.types.Message, state: FSMContext):
    groups = Schedule.get_groups(db.get_faculty(message.from_user.id), db.get_course(message.from_user.id))
    if not is_correct_group(message, groups.keys()):
        await message.answer(INCORRECT_GROUP_MESSAGE)
        await state.set_state(RegistrationForm.GROUP_WAITING)
        db.update_state(message.from_user.id, 'GROUP_WAITING')
    else:
        await message.answer(CORRECT_GROUP_MESSAGE)
        await state.set_state(RegistrationForm.REGISTERED)
        db.update_group(message.from_user.id, message.text, groups)
        db.update_state(message.from_user.id, 'REGISTERED')
        await message.answer(SUCCESS_REGISTER_MESSAGE)


