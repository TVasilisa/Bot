from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import Database
from bot_config import database

review_router = Router()

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
    await state.clear()
    await message.answer("Спасибо за ваш отзыв")
