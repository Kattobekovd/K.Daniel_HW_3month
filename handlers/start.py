from aiogram import Router, types, F
from aiogram.filters.command import Command


start_router = Router()


@start_router.message(Command('start'))
async def start_command_handler(message: types.Message):
    # print(vars(message.from_user))
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='О нас', callback_data='about_us'),
                types.InlineKeyboardButton(text='Наш адресс', callback_data='our_address')
            ],
            [
                types.InlineKeyboardButton(text='Наш сайт', url='https://taplink.cc/sushibosskg?fbclid=PAZXh0bgNhZW0CMTEAAab3dQynLXzVfoEBeef1mHqR0K5aztcSLictp2qTdivvFlX0VftL2ohUhvA_aem_2lYHuAg7JkrjEZ0C9GlMFg'),
                types.InlineKeyboardButton(text='Наш инстаграм', url='https://www.instagram.com/sushi_bosskg?igsh=czZqMWJlaXNyamIx')
            ],
            [
                types.InlineKeyboardButton(text='Контакты ', callback_data='contact'),
                types.InlineKeyboardButton(text='Вакансии', callback_data='vacancies'),

            ],
            [
                types.InlineKeyboardButton(text="Оставить отзыв", callback_data='feedback'),
            ]
        ]
    )
    await message.answer(f"""
    Привет, {message.from_user.username}! Я ваш Бот помощник от ресторана "СушиБосс".

    **Наше меню включает:**
    - Суши и роллы
    - Пицца
    - Закуски
    - Напитки

    Вы можете выбрать один из наших специальных сетов. Просто напишите название сета, и мы предоставим вам фото и описание:

    - **Сет напитков**: освежающие коктейли.
    - **Сет пицц**: классические и авторские рецепты.
    - **Сет суши**: разнообразные роллы и нигири.
    
    **Особые возможности:**
    - Напишите "Хочу рецепт", и мы поделимся с вами случайным фирменным рецептом!

    **Команды:**
    - `/start` - начать работу

    Если у вас есть особые пожелания или вопросы, дайте нам знать. Приятного аппетита! 🍣🍕
    """, reply_markup=keyboard)


@start_router.callback_query(F.data == 'about_us')
async def about_us_handler(callback: types.CallbackQuery):
    await callback.message.answer('График работы: ‌с 10:00 до 23:00 '
                                  'Бесплатная доставка от 1000 сом ‌в радиус 5км от нашего заведения')


@start_router.callback_query(F.data == 'our_address')
async def our_address_handler(callback: types.CallbackQuery):
    await callback.message.answer('Bishkek, Moskovskaya 159')


@start_router.callback_query(F.data == 'contact')
async def contact_handler(callback: types.CallbackQuery):
    await callback.message.answer('+996 556 600 099')


@start_router.callback_query(F.data == 'vacancies')
async def vacancies_handler(callback: types.CallbackQuery):
    await callback.message.answer('К сожелению в данный момент вакансии нету!')


