from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext # <---
from aiogram.fsm.state import State, StatesGroup # <---


user = Router()

class HotelState(StatesGroup):
    waiting_for_name = State()
    waiting_for_room = State()
    waiting_for_date = State()
    waiting_for_phone = State()


@user.message(CommandStart())
async def start(message: Message):
    await message.answer('Добро пожаловать!')


@user.message(Command('reserv'))
async def get_name(message: Message, state: FSMContext):
    await state.set_state(HotelState.waiting_for_name)
    await message.answer('Бронь номера в отеле "Hilton"')
    await message.answer('Пожалуйста, введите ФИО')


@user.message(HotelState.waiting_for_name)
async def get_room(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(HotelState.waiting_for_room)
    # Демонстрировать имеющиеся комнаты через ReplyKeyboard
    # Пример: Люкс/Обычный/Президентский/VIP
    await message.answer('Введите желаемую комнату:')


@user.message(HotelState.waiting_for_room)
async def get_date(message: Message, state: FSMContext):
    await state.update_data(room=message.text)
    await state.set_state(HotelState.waiting_for_date)
    await message.answer('Укажите дату заселения:')


@user.message(HotelState.waiting_for_date)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(HotelState.waiting_for_phone)
    await message.answer('Номер для связи:')


@user.message(HotelState.waiting_for_phone)
async def finish(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    print(data)
    await state.clear()
    await message.answer('Спасибо за бронь!')
    # Создать 2 кнопки InlineKeyboard с вариантами ответа:
    # Да - Нет
    # Создать хендер который сработает при ответе - "Да" и сохранит...
    # полученную информацию в текстовый файл (client.txt)
    # Если ответ "Нет", то должен сработать другой хендлер который...
    # отправить сообщение с рекомендацией повторить бронь через /reserv
    await message.answer(
        'Подтвердите корректность данных:\n\n'
        f'ФИО: {data.get('name')}\n'
        f'Комната: {data.get('room')}\n'
        f'Дата: {data.get('date')}\n'
        f'Телефон: {data.get('phone')}'
    )




