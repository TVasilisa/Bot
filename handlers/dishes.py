from aiogram import Router, F, types
from pprint import pprint

from bot_config import database

menu_router = Router()


@menu_router.callback_query(F.data == 'menu')
async def menu_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('Наше меню: ')
    dishes_list = database.get_all_dishes()
    pprint(dishes_list)
    for dish in dishes_list:
        await callback.message.answer(f'Название: {dish.get("dish_name")}\n'
                                      f'Цена: {dish.get("price")}')
