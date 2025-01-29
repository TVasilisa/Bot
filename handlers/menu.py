from pprint import pprint

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot_config import database

menu_item_router = Router()


class Menu(StatesGroup):
    dish_name = State()
    description = State()
    price = State()
    category = State()
    serving_size = State()
    dish_image = State()


@menu_item_router.message(Command('menu'))
async def start_menu(message: types.Message, state: FSMContext):
    await message.answer('Добавляем новое блюдо...')
    await message.answer("Введите название блюда:")
    await state.set_state(Menu.dish_name)


@menu_item_router.message(Menu.dish_name)
async def process_dish_name(message: types.Message, state: FSMContext):
    dish_name = message.text
    await state.update_data(dish_name=dish_name)
    await message.answer('Введите описание блюда:')
    await state.set_state(Menu.description)


@menu_item_router.message(Menu.description)
async def process_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer('Загрузите фото блюда: ')
    await state.set_state(Menu.dish_image)


@menu_item_router.message(Menu.dish_image, F.photo)
async def process_image(message: types.Message, state: FSMContext):
    dishes_images = message.photo
    pprint(dishes_images)
    biggest_image = dishes_images[-1]
    await state.update_data(dish_image=biggest_image.file_id)
    await message.answer('Введите цену блюда:')
    await state.set_state(Menu.price)


@menu_item_router.message(Menu.price)
async def process_price(message: types.Message, state: FSMContext):
    price = message.text
    try:
        price = float(price)
    except ValueError:
        await message.answer("Вводите только числа ")
        return

    if price <= 0:
        await message.answer("Вводите только положительную цену")
        return

    await state.update_data(price=price)
    await message.answer(
        'Выберите категорию блюда (первое, второе, пицца, напитки, салаты, горячительные напитки):')
    await state.set_state(Menu.category)


@menu_item_router.message(Menu.category)
async def process_category(message: types.Message, state: FSMContext):
    category = message.text.lower()

    menu_categories = ['первое', 'второе', 'пицца', 'напитки', 'салаты',
                       'горячительные напитки']

    if category in menu_categories:
        await state.update_data(category=category)
        await message.answer('Введите размер порции(детская или стандартная):')
        await state.set_state(Menu.serving_size)
    else:
        await message.answer(
            'Таких данных о категории нет. Пожалуйста, выберите одну из следующих категорий: первое, второе, пицца, напитки, салаты, горячительные напитки')
        await message.answer('Введите правильную категорию блюда:')
        await state.set_state(Menu.category)


@menu_item_router.message(Menu.serving_size)
async def process_serving_size(message: types.Message, state: FSMContext):
    serving_size = message.text.lower()

    valid_sizes = ['детская', 'стандартная']

    if serving_size in valid_sizes:
        await state.update_data(serving_size=serving_size)
        await message.answer(f"Блюдо добавлено в меню")
        data = await state.get_data()
        database.save_menu_item(data)
        print(data)

        await state.clear()
    else:
        await message.answer("Таких данных о размере порции нет. Пожалуйста, выберите 'детская' или 'стандартная'.")
        await message.answer('Введите правильный размер порции:')
        await state.set_state(Menu.serving_size)
