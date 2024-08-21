import asyncio
import logging

from bot_config import bot, dp, db
from handlers.start import start_router
from handlers.myinfo import myinfo_router
from handlers.random_recipe import random_recipe_router
from handlers.dishes import dishes_router
from handlers.review_dialog import review_router
from handlers.menu import menu_router


async def on_startup(bot):
    print("Бот запустился")
    db.create_tables()


async def main():
    dp.include_router(start_router)
    dp.include_router(review_router)
    dp.include_router(myinfo_router)
    dp.include_router(dishes_router)
    dp.include_router(random_recipe_router)
    dp.include_router(menu_router)

    dp.startup.register(on_startup)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
