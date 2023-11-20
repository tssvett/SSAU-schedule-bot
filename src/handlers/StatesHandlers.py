import aiogram.types
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from src.BotFile import dp
from src.MessagesFile import START_REGISTER_MESSAGE, INCORRECT_FACULTY_MESSAGE, CORRECT_FACULTY_MESSAGE, INCORRECT_COURSE_MESSAGE\
    , CORRECT_COURSE_MESSAGE, INCORRECT_GROUP_MESSAGE, CORRECT_GROUP_MESSAGE, SUCCESS_REGISTER_MESSAGE


class RegistrationForm(StatesGroup):
    FACULTY_WAITING = State()
    COURSE_WAITING = State()
    GROUP_WAITING = State()
    FINISH = State()


def is_correct_faculty(message: aiogram.types.Message):
    return True


def is_correct_group(message: aiogram.types.Message):
    return True


def is_correct_course(message: aiogram.types.Message):
    return message.text in ['1', '2', '3', '4', '5']


@dp.message(Command('register'))
async def start_state(message: aiogram.types.Message, state: FSMContext):
    await message.answer(START_REGISTER_MESSAGE)
    await state.set_state(RegistrationForm.FACULTY_WAITING)


@dp.message(RegistrationForm.FACULTY_WAITING)
async def faculty_choose(message: aiogram.types.Message, state: FSMContext):
    if not is_correct_faculty(message):
        await message.answer(INCORRECT_FACULTY_MESSAGE)
        await state.set_state(RegistrationForm.FACULTY_WAITING)
    else:
        await message.answer(CORRECT_FACULTY_MESSAGE)
        await state.set_state(RegistrationForm.COURSE_WAITING)


@dp.message(RegistrationForm.COURSE_WAITING)
async def faculty_choose(message: aiogram.types.Message, state: FSMContext):
    if not is_correct_course(message):
        await message.answer(INCORRECT_COURSE_MESSAGE)
        await state.set_state(RegistrationForm.COURSE_WAITING)
    else:
        await message.answer(CORRECT_COURSE_MESSAGE)
        await state.set_state(RegistrationForm.GROUP_WAITING)


@dp.message(RegistrationForm.GROUP_WAITING)
async def group_choose(message: aiogram.types.Message, state: FSMContext):
    if not is_correct_group(message):
        await message.answer(INCORRECT_GROUP_MESSAGE)
        await state.set_state(RegistrationForm.GROUP_WAITING)
    else:
        await message.answer(CORRECT_GROUP_MESSAGE)
        await message.answer(SUCCESS_REGISTER_MESSAGE)


