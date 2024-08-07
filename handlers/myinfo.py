from aiogram import Router, types, F
from aiogram.filters.command import Command

myinfo_router = Router()
@myinfo_router.message(Command('myinfo'))
async def user_info(message: types.Message):
    await message.answer(f'Вот ваши данные id: {message.from_user.id}, '
                         f'Имя: {message.from_user.first_name},'
                         f'username: {message.from_user.username}')
