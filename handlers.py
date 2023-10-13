import aiogram
import os

import config
from bot import dp, telebot, autojoin
from buttons import schedule_buttons
from utility import picture_choose, day_calc
from Schedule import Schedule
from CustomOutput import CustomOutput
from config import DEAD_MESSAGE
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class AutoState(StatesGroup):
    waiting_for_name = State()
    waiting_for_lecture = State()
def group_choose(day, message):
    if message.from_user.id == config.polina_id:
        schedule = Schedule(day_number=day, group_id=701780995)
    else:
        schedule = Schedule(day_number=day, group_id=799359428)
    return schedule


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


@dp.message_handler(lambda message: message.text.lower() == 'айди')
async def show_id(message: aiogram.types.Message):
    print(message.from_user.id)
    await message.answer(f'Ваш айди: {message.from_user.id}')


@dp.message_handler(lambda message: message.text.lower() == 'сегодня')
async def today_schedule(message: aiogram.types.Message):
    schedule = group_choose(0, message)
    picture = picture_choose()
    if schedule.is_alive:
        out = CustomOutput(schedule.get_week())
        await telebot.send_photo(message.chat.id, picture, caption=out.day(day_calc()), parse_mode='html')
    else:
        await telebot.send_photo(message.chat.id, picture, caption=DEAD_MESSAGE)


@dp.message_handler(lambda message: message.text.lower() == 'завтра')
async def tomorrow_schedule(message: aiogram.types.Message):
    schedule = group_choose(1, message)
    picture = picture_choose()
    if schedule.is_alive:
        out = CustomOutput(schedule.get_week())
        await telebot.send_photo(message.chat.id, picture, caption=out.day(day_calc(1)), parse_mode='html')
    else:
        await telebot.send_photo(message.chat.id, picture, caption=DEAD_MESSAGE)


@dp.message_handler(lambda message: message.text.lower() == 'послезавтра')
async def double_tomorrow_schedule(message: aiogram.types.Message):
    schedule = group_choose(2, message)
    picture = picture_choose()
    if schedule.is_alive:
        out = CustomOutput(schedule.get_week())

        await telebot.send_photo(message.chat.id, picture, caption=out.day(day_calc(2)), parse_mode='html')
    else:
        await telebot.send_photo(message.chat.id, picture, caption=DEAD_MESSAGE)


@dp.message_handler(lambda message: message.text.lower() == 'текущая неделя')
async def current_week_schedule(message: aiogram.types.Message):
    schedule = group_choose(0, message)
    picture = picture_choose()
    if schedule.is_alive:
        out = CustomOutput(schedule.get_week())
        part1, part2 = out.weeke()
        await telebot.send_message(message.chat.id, part1 + part2, disable_web_page_preview=True)
    else:
        await telebot.send_photo(message.chat.id, picture, caption=DEAD_MESSAGE)



@dp.message_handler(lambda message: message.text.lower() == 'следующая неделя')
async def next_week_schedule(message: aiogram.types.Message):
    schedule = group_choose(7, message)
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

@dp.message_handler(lambda message: message.text.lower() == 'коннект')
async def random(message: aiogram.types.Message):
    autojoin.set_message(message)
    await autojoin.start_session()
    await autojoin.end_session()
    await autojoin.check_status()

@dp.message_handler(lambda message: message.text.lower() == 'статус')
async def random(message: aiogram.types.Message):
    autojoin.set_message(message)
    await autojoin.check_status()

@dp.message_handler(lambda message: message.text.lower() == 'выйди')
async def random(message: aiogram.types.Message):
    autojoin.set_message(message)
    await autojoin.check_status()
    await autojoin.end_session()
    await autojoin.check_status()

@dp.message_handler(lambda message: message.text.lower() == 'лекция')
async def random(message: aiogram.types.Message, state: FSMContext):
    await telebot.send_message(message.chat.id, 'Введите имя, отображаемое на лекции')
    await state.set_state(AutoState.waiting_for_name.state)

@dp.message_handler(state=AutoState.waiting_for_name)
async def random(message: aiogram.types.Message, state: FSMContext):
    autojoin.set_name(message.text)
    await state.set_state(AutoState.waiting_for_lecture.state)
    await telebot.send_message(message.chat.id, 'Введите лекцию, на которкую нужно зайти.')

@dp.message_handler(state=AutoState.waiting_for_lecture)
async def random(message: aiogram.types.Message, state: FSMContext):
    if message.text not in autojoin.allowed:
        await telebot.send_message(message.chat.id, f'Такой лекции нет. Список доступных:\n {autojoin.allowed}')
        return
    autojoin.set_lecture(message.text)
    await state.finish()
    await telebot.send_message(message.chat.id, 'Все хорошо, можете писать "коннект"')


@dp.message_handler(lambda message: message.text.lower() == 'отмена', state="*")
async def random(message: aiogram.types.Message, state: FSMContext):
    await state.finish()
    await telebot.send_message(message.chat.id, 'Действие успешно отменено')



