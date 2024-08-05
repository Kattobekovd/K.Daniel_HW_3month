import asyncio
from random import choice
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv
from os import getenv


load_dotenv()
token = getenv('BOT_TOKEN')
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_command_handler(message: types.Message):
    print(vars(message.from_user))
    await message.answer(f'Привет {message.from_user.username}')


@dp.message(Command('myinfo'))
async def user_info(message: types.Message):
    await message.answer(f'Вот ваши данные id: {message.from_user.id}, '
                         f'Имя: {message.from_user.first_name},'
                         f'username: {message.from_user.username}')


recipe_list = ['1 Салат Капрезе Ингредиенты: помидоры, моцарелла, базилик, оливковое масло, бальзамический уксус.'
               'Приготовление: нарезать помидоры и моцареллу, выложить слоями, добавить базилик, полить оливковым маслом и уксусом.',
               '2. Омлет с сыром и зеленью Ингредиенты: яйца, сыр, зелень, соль, перец.'
               'Приготовление: взбить яйца, добавить тертый сыр и нарезанную зелень, приправить, жарить на сковороде до готовности.',
               '3. Паста с чесноком и оливковым маслом Ингредиенты: спагетти, чеснок, оливковое масло, петрушка, сыр пармезан.'
               'Приготовление: отварить спагетти, обжарить чеснок в масле, добавить пасту и петрушку, посыпать пармезаном.',
               '4. Куриное филе с лимоном Ингредиенты: куриное филе, лимон, соль, перец, оливковое масло.'
               'Приготовление: обжарить филе на масле, добавить сок лимона, приправить, тушить до готовности.',
               '5. Греческий йогурт с ягодами Ингредиенты: греческий йогурт, ягоды, мед, орехи.'
               'Приготовление: выложить йогурт в чашку, добавить ягоды, полить медом и посыпать орехами.']


@dp.message(Command('random_recipe'))
async def random_recipe(message: types.Message):
    await message.answer(choice(recipe_list))


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
