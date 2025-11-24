from aiogram import BaseMiddleware
from typing import Callable, Dict, Awaitable, Any
from aiogram.types import Message





class CheckAdmin(BaseMiddleware):
    def __init__(self):
        self.admins = [795638945, 1811521216]

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id not in self.admins:
            await event.answer('ты не админ теряйся фрик')
            return

        return await handler(event, data)

