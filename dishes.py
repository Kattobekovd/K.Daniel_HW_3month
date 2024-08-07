from aiogram import Router, types, F
from aiogram.filters.command import Command


dishes_router = Router()
@dishes_router.message(F.text == 'Сет напитков')
async def dishes_handler(message: types.Message):
    image = types.FSInputFile('images/beverages.jpg')
    await message.answer_photo(
        photo=image,
        caption='Кола,Фанта,Спрайт  100сомов'
    )

@dishes_router.message(F.text == 'Сет пицц')
async def dishes_handler(message: types.Message):
    image = types.FSInputFile('images/pizza.jpg')
    await message.answer_photo(
        photo=image,
        caption='Курабро,Марфа,Брынза,ДОмашняя,Боясркая 1499сомов'
    )

@dishes_router.message(F.text == 'Сет суши')
async def dishes_handler(message: types.Message):
    image = types.FSInputFile('images/sushi.jpg')
    await message.answer_photo(
        photo=image,
        caption='Филодельфия 990сомов'
    )
