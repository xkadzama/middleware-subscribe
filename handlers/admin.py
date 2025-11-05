from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


admin = Router()

class RoomsState(StatesGroup):
    waiting_for_category = State()
    waiting_for_amount_people = State()
    waiting_for_price = State()
    waiting_for_status = State()
    waiting_for_photo = State()

@admin.message(Command('admin_info'))
async def admin_start(message: Message):
    await message.answer('Напишите или нажмите на команду "/rooms" она добовляет комнаты в таблицу')

@admin.message(Command('rooms'))
async def add_rooms(message: Message, state: FSMContext):
    await state.set_state(RoomsState.waiting_for_category)
    await message.answer('укажите котегорию комнаты')

@admin.message(RoomsState.waiting_for_category)
async def amount_people(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(RoomsState.waiting_for_amount_people)
    await message.answer('укажите вместимость людей для номера')

@admin.message(RoomsState.waiting_for_amount_people)
async  def room_price(message: Message, state: FSMContext):
    await state.update_data(amout_people=message.text)
    await state.set_state(RoomsState.waiting_for_price)
    await message.answer('укажите цену за сутки')

@admin.message(RoomsState.waiting_for_price)
async def rooms_status(message: Message, state: FSMContext):
    await state.update_data(price = message.text)
    await state.set_state(RoomsState.waiting_for_status)
    await message.answer('укажите занята ли комната если занята то напишите укажите цифрами если заната то цифра "1" в ином случае цифра "2"')

@admin.message(RoomsState.waiting_for_status)
async def room_photo(message: Message, state: FSMContext):
    await state.update_data(status = message.text)
    await state.set_state(RoomsState.waiting_for_photo)
    await message.answer('Отправьте фото комнаты')

@admin.message(RoomsState.waiting_for_photo)
async def finish(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo)
    rooms_table = await state.get_data()
    await message.answer('комната добавлена в таблицу!')
    await message.answer('продтвердите корректность\n\n'
                         f'категория {rooms_table.get('category')}\n'
                         f'кол-во людей {rooms_table.get('amout_people')}\n'
                         f'цена {rooms_table.get('price')}\n'
                         f'статус {rooms_table.get('status')}\n'
                         f'фото {rooms_table.get('photo')}'
                         )