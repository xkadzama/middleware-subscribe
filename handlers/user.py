from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, MessageReactionUpdated
import sqlite3
import os
from database.db import db_reactor

from pyexpat.errors import messages

user = Router()


# @user.message(CommandStart())
# async def start_bot(message: Message):
#     await message.answer('Добро пожаловать!')


@user.message(Command('rooms'))
async def rooms_info(message: Message):
    conn = sqlite3.connect('rooms.db')
    print(message)
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
    print(message)
    conn.commit()
    conn.close()

@user.message_reaction()
async def handle_reaction(reaction_update: MessageReactionUpdated):
    user_id = reaction_update.user.id
    chat_id = reaction_update.chat.id
    message_id = reaction_update.message_id

    bot = Bot(token=os.getenv('API'))

    try:
        message = await bot.forward_message(chat_id, chat_id, message_id)
        message_text = message.text if message.text else message.caption

        room_id = None
        if message_text and 'ID комнаты:' in message_text:
            for line in message_text.split('\n'):
                if 'ID комнаты:' in line:
                    room_id = int(line.split(':')[1].strip())
                    break

        if not room_id:
            room_id = message_id

        reaction_emoji = None
        if reaction_update.new_reaction:
            reaction_emoji = str(reaction_update.new_reaction[0].emoji) if reaction_update.new_reaction else None

        success = db_reactor.add_reaction(user_id, room_id, reaction_emoji)

        if success:
            print(f"Reaction saved: user {user_id}, room {room_id}, reaction {reaction_emoji}")
        else:
            print(f"Failed to save reaction for user {user_id}")

    except Exception as e:
        print(f"Error processing reaction: {e}")
    finally:
        await bot.session.close()

