import json
import os

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (Message,
                           KeyboardButton,
                           CallbackQuery,
                           FSInputFile,
                           ReplyKeyboardMarkup,
                           KeyboardButtonRequestUser,
                           InlineKeyboardButton,
                           ReplyKeyboardRemove)
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
        [KeyboardButton(text='Luxe'), KeyboardButton(text='Standard')],
        [KeyboardButton(text='President'), KeyboardButton(text='Vip')]
    ]
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await state.update_data(name=message.text)
    await state.set_state(HotelState.waiting_for_room)
    await message.answer('Введите желаемую комнату:', reply_markup=markup)


@user.message(HotelState.waiting_for_room)
async def get_date(message: Message, state: FSMContext):
    await state.update_data(room=message.text)
    await state.set_state(HotelState.waiting_for_date)
    await message.answer('Укажите дату заселения:', reply_markup=ReplyKeyboardRemove())


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
    await state.update_data(tg_id=message.from_user.id)
    data = await state.get_data()
    await message.answer('Спасибо за бронь!')
    await message.answer(
        'Подтвердите корректность данных:\n\n'
        f'ФИО: {data.get('name')}\n'
        f'Комната: {data.get('room')}\n'
        f'Дата: {data.get('date')}\n'
        f'Телефон: {data.get('phone')}',
        reply_markup=kb.as_markup()
    )

@user.callback_query(F.data == 'okey')
async def approve(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data() # <--- отсутствовал await
    await state.clear()

    filename = 'client.json'

    # Загружаем существующий список или создаём новый
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                items = json.load(f)
            except json.JSONDecodeError:
                items = []
    else:
        items = []

    items.append(data)

    # Перезаписываем файл целиком
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=4, ensure_ascii=False)

    await callback.message.edit_text('Номер зарезервирован!')


@user.callback_query(F.data == 'reserv')
async def repeat(callback: CallbackQuery):
    await callback.message.edit_text('Повторите процесс бронирования - /reserv')



# 1. Сохранять данные в формате JSON