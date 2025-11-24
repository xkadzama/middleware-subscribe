import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from states.reserve_room import reserve as reserve_fsm
from states.add_rooms import add as add_fsm
from handlers.admin import admin as admin_router
from handlers.user import user as user_router
from database.db import db_manager
from database.db import db_reactor
from meddleware.mdw import CheckAdmin


load_dotenv()
bot = Bot(token=os.getenv('API'))
dp = Dispatcher()

dp.include_routers(
    reserve_fsm, add_fsm,
    admin_router, user_router
)
add_fsm.message.middleware.register(CheckAdmin())


async def main():
    print('FORCE I RUN')
    db_manager.init_database()
    db_reactor.init_database()
    await dp.start_polling(bot)
    print('FORCE I STOPPED')


if __name__ == '__main__':
    asyncio.run(main())