from Tools.i18n.makelocalealias import pprint
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import Database
from bot_config import database

review_router = Router()

menu_admin_router = Router()
ADMIN_ID = 1379406454
menu_admin_router.message.filter(F.from_user.id == ADMIN_ID)
menu_admin_router.callback_query(F.message.from_user.id == ADMIN_ID)


class RestourantReview(StatesGroup):
    name = State()
    phone_number = State()
    rate = State()
    extra_comments = State()


@review_router.message(Command("stop"))
@review_router.message(F.text == "стоп")
async def stop_dialog(message: types.Message, state: FSMContext):
    await message.answer("Диалог остановлен")
    await state.clear()


@review_router.callback_query(F.data == 'review')
async def start_review(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Оставьте жалобу ответив на несколько вопросов. Можете остановить диалог с ботом введя '/stop' или 'стоп'")
    await callback.answer()
    await callback.message.answer("Как Вас зовут?")
    await state.set_state(RestourantReview.name)


@review_router.message(RestourantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer('Укажите ваш номер телефона')
    await state.set_state(RestourantReview.phone_number)


@review_router.message(RestourantReview.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    await message.answer('Пожалуйста, поставьте оценку обслуживанию (от 1 до 5 баллов)')
    await state.set_state(RestourantReview.rate)


@review_router.message(RestourantReview.rate)
async def process_rate(message: types.Message, state: FSMContext):
    try:
        rate = int(message.text)
        if 1 <= rate <= 5:
            await state.update_data(rate=rate)
            await state.set_state(RestourantReview.extra_comments)
            await message.answer('Опишите ваш опыт')
        else:
            await message.answer("Пожалуйста, поставьте оценку от 1 до 5")
    except ValueError:
        await message.answer("Пожалуйста, введите корректную оценку от 1 до 5")


@review_router.message(RestourantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    extra_comments = message.text
    await state.update_data(extra_comments=extra_comments)
    data = await state.get_data()
    database.save_review(data)
    await message.answer("Спасибо за ваш отзыв")
    await state.clear()


@menu_admin_router.callback_query(F.data == 'admin_review', F.from_user.id == ADMIN_ID)
async def admin_review_handler(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.message.answer("У вас нет прав для просмотра отзывов")
        return

    summary_of_review = database.get_all_reviews()

    if not summary_of_review:
        await callback.message.answer("Отзывов пока нет.")
        return

    for review in summary_of_review:
        name = review.get("name")
        phone_number = review.get("phone_number")
        rate = review.get("rate")
        extra_comments = review.get("extra_comments")

        message = f"Отзыв от {name}:\nТелефон: {phone_number}:\nОценка: {rate}\nКомментарий: {extra_comments}\n"

        await callback.message.answer(message)



