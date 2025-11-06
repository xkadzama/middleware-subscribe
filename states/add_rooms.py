from aiogram.fsm.state import State, StatesGroup

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database.db import db_manager

add = Router()


class RoomsState(StatesGroup):
    waiting_for_category = State()
    waiting_for_amount_people = State()
    waiting_for_price = State()
    waiting_for_status = State()
    waiting_for_photo = State()


@add.message(Command('admin_info'))
async def admin_start(message: Message):
    await message.answer('Напишите или нажмите на команду "/add_rooms" она добовляет комнаты в таблицу')


@add.message(Command('add_rooms'))
async def add_rooms(message: Message, state: FSMContext):
    await state.set_state(RoomsState.waiting_for_category)
    await message.answer('укажите котегорию комнаты')


@add.message(RoomsState.waiting_for_category)
async def amount_people(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(RoomsState.waiting_for_amount_people)
    await message.answer('укажите вместимость людей для номера')


@add.message(RoomsState.waiting_for_amount_people)
async  def room_price(message: Message, state: FSMContext):
    await state.update_data(amount_people=message.text)
    await state.set_state(RoomsState.waiting_for_price)
    await message.answer('укажите цену за сутки')


@add.message(RoomsState.waiting_for_price)
async def rooms_status(message: Message, state: FSMContext):
    await state.update_data(price = message.text)
    await state.set_state(RoomsState.waiting_for_status)
    await message.answer('укажите занята ли комната если занята то напишите укажите цифрами если заната то цифра "1" в ином случае цифра "0"')


@add.message(RoomsState.waiting_for_status)
async def room_photo(message: Message, state: FSMContext):
    await state.update_data(status=message.text)
    await state.set_state(RoomsState.waiting_for_photo)
    await message.answer('Отправьте фото комнаты')


@add.message(RoomsState.waiting_for_photo, F.photo)
async def finish(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    rooms_data = await state.get_data()
    success = db_manager.add_rooms(
        category=rooms_data.get('category'),
        amount_people=rooms_data.get('amount_people'),
        price=rooms_data.get('price'),
        status=rooms_data.get('status'),
        photo_id=photo_id
    )

    if success:
        await message.answer('Комната добавлена в таблицу!')
        await message.answer(
            'Подтвердите корректность:\n\n'
            f'Категория: {rooms_data.get("category")}\n'
            f'Кол-во людей: {rooms_data.get("amount_people")}\n'
            f'Цена: {rooms_data.get("price")} руб.\n'
            f'Статус: {"Занята" if rooms_data.get("status") == 1 else "Свободна"}\n'
            f'Фото: добавлено'
        )
    else:
        await message.answer('Ошибка при добавлении комнаты в базу данных')

    await state.clear()