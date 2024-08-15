from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot_config import database

review_router = Router()


class ReviewDialog(StatesGroup):
    name = State()
    contact = State()
    visit_date = State()
    food_rating = State()
    cleanliness_ratting = State()
    extra_comments = State()


@review_router.callback_query(F.data == 'feedback')
async def start_survey(callback: types.Message, state: FSMContext):
    await state.set_state(ReviewDialog.name)
    await callback.message.answer ('Как вас зовут?')


@review_router.message(ReviewDialog.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ReviewDialog.contact)
    await message.answer('Ваш номер телефона или инстаграмм?')


@review_router.message(ReviewDialog.contact)
async def process_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(ReviewDialog.visit_date)
    await message.answer('Дата вашего посещения нашего заведения?')


@review_router.message(ReviewDialog.visit_date)
async def process_contact(message: types.Message, state: FSMContext):
    visit_date = message.text
    if not visit_date.isdigit():
        await message.answer('Введите только цифры')
        return
    visit_date = int(visit_date)
    await state.update_data(visit_date=visit_date)
    await state.set_state(ReviewDialog.food_rating)

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Отлично", callback_data="excellent"),
                types.InlineKeyboardButton(text="Хорошо", callback_data="good"),
            ],
            [
                types.InlineKeyboardButton(text="Удовлетворительно", callback_data="ok"),
                types.InlineKeyboardButton(text="Плохо", callback_data="bad"),
            ]
        ]
    )
    await message.answer('Как вы оцениваете качество еды?', reply_markup=kb)


@review_router.callback_query(F.data == 'excellent')
@review_router.callback_query(F.data == 'good')
@review_router.callback_query(F.data == 'ok')
@review_router.callback_query(F.data == 'bad')
async def food_rating(callback: types.CallbackQuery,state: FSMContext):
    processing_rating = {
        "excellent": "Отлично! Мы рады, что вам понравилось!",
        "good": "Хорошо! Спасибо за ваш отзыв!",
        "ok": "Спасибо за отзыв! Мы учтём ваши пожелания.",
        "bad": "Сожалеем, что вам не понравилось. Мы постараемся улучшить качество."
    }
    await callback.message.answer(processing_rating[callback.data])
    await state.update_data(food_rating=callback.data)
    await state.set_state(ReviewDialog.cleanliness_ratting)

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Отлично", callback_data="cleanliness_excellent"),
                types.InlineKeyboardButton(text="Хорошо", callback_data="cleanliness_good"),
            ],
            [
                types.InlineKeyboardButton(text="Удовлетворительно", callback_data="cleanliness_ok"),
                types.InlineKeyboardButton(text="Плохо", callback_data="cleanliness_bad"),
            ]
        ]
    )
    await callback.message.answer ('Как вы оцениваете чистоту заведение ?', reply_markup=kb)


#здесь мы проверяем обработваем на случаи если юзер место кнопок напишет комент
@review_router.message(ReviewDialog.food_rating)
async def handle_food_rating_text(message: types.Message, state: FSMContext):
    await message.answer("Спасибо за отзыв! Продолжаем опрос.")
    await state.set_state(ReviewDialog.cleanliness_ratting)
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Отлично", callback_data="cleanliness_excellent"),
                types.InlineKeyboardButton(text="Хорошо", callback_data="cleanliness_good"),
            ],
            [
                types.InlineKeyboardButton(text="Удовлетворительно", callback_data="cleanliness_ok"),
                types.InlineKeyboardButton(text="Плохо", callback_data="cleanliness_bad"),
            ]
        ]
    )
    await message.answer('Как вы оцениваете чистоту заведения?', reply_markup=kb)


@review_router.callback_query(F.data == 'cleanliness_excellent')
@review_router.callback_query(F.data == 'cleanliness_good')
@review_router.callback_query(F.data == 'cleanliness_ok')
@review_router.callback_query(F.data == 'cleanliness_bad')
async def process_cleanliness_ratting(callback: types.CallbackQuery, state: FSMContext):
    processing_cleanliness_ratting = {
        "cleanliness_excellent": "Отлично! Мы рады, что вам понравилось!",
        "cleanliness_good": "Спасибо за ваш отзыв!",
        "cleanliness_ok": "Спасибо! Мы учтём ваши пожелания.",
        "cleanliness_bad": "Сожалеем, что вам не понравилось. Мы будем стараться улучшить чистоту."
    }
    await callback.message.answer(processing_cleanliness_ratting[callback.data])
    await state.update_data(cleanliness_rating=callback.data)
    await state.set_state(ReviewDialog.extra_comments)
    await callback.message.answer('Допольнительные комментарии')


#так же проверям на слаучаи текста место инлайн кнопок
@review_router.message(ReviewDialog.cleanliness_ratting)
async def handle_cleanliness_rating_text(message: types.Message, state: FSMContext):
    await message.answer("Спасибо за отзыв! Продолжаем опрос.")
    await state.set_state(ReviewDialog.extra_comments)
    await message.answer('Дополнительные комментарии?')


@review_router.message(ReviewDialog.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    await message.answer('Cпасибо за оставленный отзыв!')
    data = await state.get_data()
    print(data)

    database.execute(
        query="INSERT INTO survey_results (name, contact, visit_date, food_rating, cleanliness_rating, additional_comments) VALUES (?, ?, ?, ?, ?, ?)",
        params=(
            data.get('name'),
            data.get('contact'),
            data.get('visit_date'),
            data.get('food_rating'),
            data.get('cleanliness_rating'),
            data.get('additional_comments')
        )
    )

    await state.clear()








