import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers.reserve_fsm import reserve as reserve_router
from middlewares.subscribe import SubscribeMiddleware

load_dotenv()
bot = Bot(token=os.getenv('API'))
dp = Dispatcher()
dp.include_routers(reserve_router)
# user_router.message.middleware(SubscribeMiddleware(bot=bot, chat_id=-1003244158184))

async def main():
    print('FORCE I RUN')
    await dp.start_polling(bot)
    print('FORCE I STOPPED')



# ~dfsf
if __name__ == '__main__':
    asyncio.run(main())