from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from os import getenv
from database.database import Database

load_dotenv()
token = getenv('BOT_TOKEN')
bot = Bot(token=token)
dp = Dispatcher()
db = Database('db.sqlite3')


async def set_bot_commands():
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Начало"),
        types.BotCommand(command="menu", description='Меню')
    ])
