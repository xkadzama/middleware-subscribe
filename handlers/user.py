from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (Message,
                           KeyboardButton,
                           CallbackQuery,
                           FSInputFile,
                           ReplyKeyboardMarkup,
                           KeyboardButtonRequestUser,
                           InlineKeyboardButton)
from aiogram.fsm.context import FSMContext # <---
from aiogram.fsm.state import State, StatesGroup # <---
from aiogram.utils.keyboard import InlineKeyboardBuilder

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
    kb = [
        [KeyboardButton(text='Luxe')],
        [KeyboardButton(text='Standard')],
        [KeyboardButton(text='President')],
        [KeyboardButton(text='Vip')]
    ]
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await state.update_data(name=message.text)
    await state.set_state(HotelState.waiting_for_room)
    # Демонстрировать имеющиеся комнаты через ReplyKeyboard
    # Пример: Люкс/Обычный/Президентский/VIP
    await message.answer('Введите желаемую комнату:', reply_markup=markup)


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
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text='Все правильно',
        callback_data='okey'
    ))
    kb.add(InlineKeyboardButton(
        text='Корректировать',
        callback_data='reserv'
    ))
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
        f'Телефон: {data.get('phone')}',
        reply_markup=kb.as_markup()
    )

@user.callback_query(F.data == 'okey')
async def okey(callback: CallbackQuery, state: FSMContext):
    data = state.get_data()
    await callback.answer('Номер зарезервирован!')
    with open('client.txt', mode='a', encoding='utf-8') as reserv_:
        reserv_.write(f'{data}')
    await callback.message.answer('Номер зарезервирован!')


@user.callback_query(F.data == 'reserv')
async def reserv(callback: CallbackQuery):
    kb = [KeyboardButton(text='/reserv')]
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await callback.answer('Повторите процесс бронирования!')
    await callback.message.answer('Повторите процесс бронирования!', reply_markup=markup)



