from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from os import getenv
from database.database import Database

load_dotenv()
token = getenv('BOT_TOKEN')
bot = Bot(token=token)
dp = Dispatcher()
db = Database('db.sqlite3')