from aiogram.filters import BaseFilter
from aiogram.types.message import Message
from src.Database.DatabaseClass import db


class RegisterFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return db.is_registered(message.from_user.id)
