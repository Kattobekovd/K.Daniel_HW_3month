from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot_config import db

review_router = Router()


class ReviewDialog(StatesGroup):
    name = State()
    contact = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()


@review_router.callback_query(F.data == 'feedback')
async def start_survey(callback: types.Message, state: FSMContext):
    await state.set_state(ReviewDialog.name)
    await callback.message.answer('Как вас зовут?')


@review_router.message(ReviewDialog.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ReviewDialog.contact)
    await message.answer('Ваш номер телефона или инстаграм?')


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
                types.InlineKeyboardButton(text="Отлично", callback_data="5"),
                types.InlineKeyboardButton(text="Хорошо", callback_data="4"),
            ],
            [
                types.InlineKeyboardButton(text="Удовлетворительно", callback_data="3"),
                types.InlineKeyboardButton(text="Плохо", callback_data="2"),
            ]
        ]
    )
    await message.answer('Как вы оцениваете качество еды?', reply_markup=kb)


@review_router.callback_query(ReviewDialog.food_rating)
async def food_rating(callback: types.CallbackQuery, state: FSMContext):
    print (callback.data)
    processing_rating = {
        5: "Отлично! Мы рады, что вам понравилось!",
        4: "Хорошо! Спасибо за ваш отзыв!",
        3: "Спасибо за отзыв! Мы учтём ваши пожелания.",
        2: "Сожалеем, что вам не понравилось. Мы постараемся улучшить качество."
    }
    rating = int(callback.data)
    await callback.message.answer(processing_rating[rating])
    await state.update_data(food_rating=rating)

    await state.set_state(ReviewDialog.cleanliness_rating)

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Отлично", callback_data="5"),
                types.InlineKeyboardButton(text="Хорошо", callback_data="4"),
            ],
            [
                types.InlineKeyboardButton(text="Удовлетворительно", callback_data="3"),
                types.InlineKeyboardButton(text="Плохо", callback_data="2"),
            ]
        ]
    )
    await callback.message.answer('Как вы оцениваете чистоту заведения?', reply_markup=kb)


@review_router.callback_query(ReviewDialog.cleanliness_rating)
async def process_cleanliness_rating(callback: types.CallbackQuery, state: FSMContext):
    rating = int(callback.data)
    processing_cleanliness_rating = {
        5: "Отлично! Мы рады, что вам понравилось!",
        4: "Спасибо за ваш отзыв!",
        3: "Спасибо! Мы учтём ваши пожелания.",
        2: "Сожалеем, что вам не понравилось. Мы будем стараться улучшить чистоту."
    }
    await callback.message.answer(processing_cleanliness_rating[rating])
    await state.update_data(cleanliness_rating=rating)
    await state.set_state(ReviewDialog.extra_comments)
    await callback.message.answer('Дополнительные комментарии?')


@review_router.message(ReviewDialog.food_rating)
async def handle_food_rating_text(message: types.Message, state: FSMContext):
    await message.answer("Нажмите на кнопки!!!")
    await state.set_state(ReviewDialog.food_rating)

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Отлично", callback_data="5"),
                types.InlineKeyboardButton(text="Хорошо", callback_data="4"),
            ],
            [
                types.InlineKeyboardButton(text="Удовлетворительно", callback_data="3"),
                types.InlineKeyboardButton(text="Плохо", callback_data="2"),
            ]
        ]
    )
    await message.answer('Как вы оцениваете качество еды?', reply_markup=kb)


# так же проверям на слаучаи текста место инлайн кнопок
@review_router.message(ReviewDialog.cleanliness_rating)
async def handle_cleanliness_rating_text(message: types.Message, state: FSMContext):
    await message.answer("Нажмите на кнопки!!!")
    await state.set_state(ReviewDialog.cleanliness_rating)

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Отлично", callback_data="5"),
                types.InlineKeyboardButton(text="Хорошо", callback_data="4"),
            ],
            [
                types.InlineKeyboardButton(text="Удовлетворительно", callback_data="3"),
                types.InlineKeyboardButton(text="Плохо", callback_data="2"),
            ]
        ]
    )
    await message.answer('Как вы оцениваете чистоту заведения?', reply_markup=kb)


@review_router.message(ReviewDialog.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    await message.answer('Спасибо за оставленный отзыв!')
    data = await state.get_data()
    print(data)

    db.execute(
        query="INSERT INTO survey_results (name, contact, visit_date, food_rating, cleanliness_rating, additional_comments)"
              " VALUES (?, ?, ?, ?, ?, ?)",
        params=(
            data.get('name'),
            data.get('contact'),
            data.get('visit_date'),
            data.get('food_rating'),
            data.get('cleanliness_rating'),
            data.get('extra_comments')
        )
    )

    await state.clear()
