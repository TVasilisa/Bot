from aiogram import Router, F, types
from aiogram.filters import Command
from pprint import pprint

from bot_config import database
from handlers.review_dialog import menu_admin_router

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='O нас', callback_data='about_us'),
                types.InlineKeyboardButton(text='Условия доставки', callback_data='delivery')],
            [types.InlineKeyboardButton(text='Меню', callback_data='menu')],
            [types.InlineKeyboardButton(text='Оставить отзыв', callback_data='review')],
            [types.InlineKeyboardButton(text='Просмотр отзывов', callback_data='admin_review')],
        ]
    )
    await message.answer(f"Привет, {name}", reply_markup=kb)


@start_router.callback_query(F.data == 'about_us')
async def about_us_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('Мы - стандартная кофейня в вашем городе. Ничего нового, ничего интересного')


@start_router.callback_query(F.data == 'delivery')
async def delivery_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        'Доставка стоит 150-250 сом по городу. Доставляем в течение 30-50 минут через голубей')


@start_router.callback_query(F.data == 'menu')
async def menu_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('Наше меню: ')
    dishes_list = database.get_all_dishes()
    pprint(dishes_list)
    for dish in dishes_list:
        await callback.message.answer(f'Название: {dish.get("dish_name")}\n'
                                      f'Цена: {dish.get("price")}')



