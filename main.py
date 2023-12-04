import asyncio
from src.handlers.OutputHandlers import *
from src.handlers.StatesHandlers import *
from src.handlers.AdminHandlers import *


async def main():
    await dp.start_polling(telebot)

if __name__ == '__main__':
    asyncio.run(main())
