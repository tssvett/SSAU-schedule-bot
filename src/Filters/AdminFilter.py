from aiogram.filters import BaseFilter
from src.AdminPanelClass import admin_panel
from aiogram.types.message import Message


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == admin_panel.get_admin_id()
