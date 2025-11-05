# Реализовать хендлер для демонстрации свободных номеров
# /free_rooms
# Фото комнаты / MediaBuilderGroup
# Номер: Lux/Standart/Президентский и тд
# Кол-во людей: 2
# Цена: 5000 р/сутки
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

user = Router()


@user.message(Command('rooms'))
async def rooms_info(message: Message):
    await message.answer('вот список свободных номеров:')
