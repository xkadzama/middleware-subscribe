from pyexpat.errors import messages
from typing import Callable, Any, Dict, Awaitable
from aiogram.types import Message
from aiogram import BaseMiddleware, Bot
from pydantic.v1.class_validators import all_kwargs


class SubscribeMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot, chat_id: int):
        self.bot = bot
        self.chat_id = chat_id

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> None:
        user_status = await self.bot.get_chat_member(self.chat_id, event.from_user.id)
        if user_status.status in ['creator', 'member', 'administrator']:
            return await handler(event, data)
        else:
            await event.answer('Подпишитесь на канал!')
