import asyncio
from handlers.OutputHandlers import *
from handlers.StatesHandlers import *


async def main():
    await dp.start_polling(telebot)

if __name__ == '__main__':
    asyncio.run(main())
