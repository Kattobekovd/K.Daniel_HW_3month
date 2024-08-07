import asyncio

from aiogram import Bot, Dispatcher
from bot_config import bot, dp
from handlers.start import start_router
from handlers.myinfo import myinfo_router
from handlers.random_recipe import random_recipe_router
from dishes import dishes_router

async def main():
    dp.include_router(start_router)
    dp.include_router(myinfo_router)
    dp.include_router(dishes_router)
    dp.include_router(random_recipe_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
