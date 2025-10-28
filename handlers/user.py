import sqlite3

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


user = Router()


@user.message(CommandStart())
async def start(message: Message):
    await message.answer('Добро пожаловать!')


@user.message(Command('music'))
async def send_music(message: Message):
    await message.answer('Идет скачивание...')
