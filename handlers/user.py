from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import sqlite3

user = Router()


# @user.message(CommandStart())
# async def start_bot(message: Message):
#     await message.answer('Добро пожаловать!')


@user.message(Command('rooms'))
async def rooms_info(message: Message):
    conn = sqlite3.connect('rooms.db')
    cursor = conn.cursor()
    await message.answer('вот список свободных номеров:')
    cursor.execute('SELECT * FROM rooms')
    rooms = cursor.fetchall()
    for room in rooms:
        if room[4] == 0:
            await message.answer(f'Категория: {room[1]}\n'
                  f'Кол-во людей: {room[2]}\n'
                  f'Цена:{room[3]}\n'
                  f'Статус: {'Занята' if room[4] == 1 else 'Свободна'}\n'
                  'Фото:')
            await message.answer_photo(room[5])

    conn.commit()
    conn.close()