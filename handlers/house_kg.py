from aiogram import Router, types, F
from crawler.house_kg_parsel import HouseKGParsel


house_kg_router = Router()


@house_kg_router.callback_query(F.data == 'house')
async def house_kg_handler(callback: types.CallbackQuery):
    crawler = HouseKGParsel()
    crawler.get_page()
    links = crawler.get_house_links()
    for link in links:
        await callback.message.answer(link)