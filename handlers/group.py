from aiogram import Router, types, F
from aiogram.filters.command import Command
from bot_config import bot
from datetime import timedelta

group_router = Router()
group_router.message.filter(F.chat.type != 'private')

bad_words = {"глупец", "болван", "тормоз"}


@group_router.message(Command('ban', prefix='!'))
async def ban_group_user(message:types.Message):
    print(message.text)
    print(message.from_user.first_name)
    reply = message.reply_to_message
    if reply:
        await bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=reply.from_user.id,
            until_date=timedelta(minutes=5)
        )


@group_router.message()
async def filter_bad_words(message: types.Message):
    print (message.chat.type)
    txt = message.text
    for word in bad_words:
        if word in txt.lower():
            await message.answer(f'Пользователь '
                                 f'{message.from_user.first_name} использовал запрешеные слова!!!\n'
                                 f'Действие: БАН на 5 минут'
                                 )
            await bot.ban_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                until_date=timedelta(minutes=5)
            )
            await message.delete()
            break
