from aiogram import BaseMiddleware
from typing import Callable, Dict, Awaitable, Any
from aiogram.types import Update


adminId = 79563894232

class CheckAdmin(BaseMiddleware):
    def __init__(self):
        self.admins = [adminId]

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        if event.message.from_user.id not in self.admins:
            await event.answer('ты не админ теряйся фрик')
            return

        return handler(event, data)

