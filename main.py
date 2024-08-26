import asyncio
import logging

from bot_config import bot, dp, db, set_bot_commands
from handlers import (
    private_router,
    group_router

)


async def on_startup(bot):
    print("Бот запустился")
    db.create_tables()


async def main():
    await set_bot_commands()
    dp.include_router(private_router)
    dp.include_router(group_router)

    dp.startup.register(on_startup)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

