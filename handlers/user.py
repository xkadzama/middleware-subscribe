from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


user = Router()


@user.message(CommandStart())
async def rooms_info(message: Message):
    await message.answer('Добро пожаловать!')


@user.message(Command('rooms'))
async def rooms_info(message: Message):
    await message.answer('вот список свободных номеров:')
