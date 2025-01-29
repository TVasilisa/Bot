from aiogram import Router, F, types
from pprint import pprint
from aiogram_widgets.pagination import TextPaginator
from bot_config import database

menu_router = Router()


@menu_router.callback_query(F.data == 'menu')
async def menu_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('Наше меню: ')
    dishes_list = database.get_all_dishes()
    pprint(dishes_list)
    # for dish in dishes_list:
    #     await callback.message.answer(f'Название: {dish.get("dish_name")}\n'
    #                                   f'Цена: {dish.get("price")}\n'
    #                                   f'Описание блюда: {dish.get("description")}\n'
    #                                   f'Категория блюда: {dish.get("category")}\n'
    #                                   f'Размер порции: {dish.get("serving_size")}')

    text_data = [
        f"Название: {dish.get('dish_name', 'Без названия')}\n"
        f"Цена: {dish.get('price', 'Не указана')} сом\n"
        f"Описание: {dish.get('description', 'Без описания')}\n"
        f"Категория: {dish.get('category', 'Не указана')}\n"
        f"Размер порции: {dish.get('serving_size', 'Не указан')}\n"
        for dish in dishes_list
    ]
    paginator = TextPaginator(data=text_data, router=menu_router, per_page=1)

    current_text_chunk, reply_markup = paginator.current_message_data

    await callback.message.answer(
        text=current_text_chunk,
        reply_markup=reply_markup
    )
