from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

review_router = Router()


class RestourantReview(StatesGroup):
    name = State()
    phone_number = State()
    rate = State()
    extra_comments = State()


@review_router.callback_query(F.data == 'review')
async def start_review(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Как Вас зовут?")
    await state.set_state(RestourantReview.name)


@review_router.message(RestourantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await message.answer('Укажите ваш номер телефона')
    await state.set_state(RestourantReview.phone_number)


@review_router.message(RestourantReview.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, поставьте оценку обслуживанию')
    await state.set_state(RestourantReview.rate)


@review_router.message(RestourantReview.rate)
async def process_rate(message: types.Message, state: FSMContext):
    await message.answer('Опишите ваш опыт')
    await state.set_state(RestourantReview.extra_comments)


@review_router.message(RestourantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Спасибо за ваш отзыв")
