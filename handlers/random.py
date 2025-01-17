from aiogram import Router, types
from aiogram.filters import Command
from random import choice

recipes = {
    "Латте": {
        "Рецепт": "Нагрейте молоко, взбейте его до пены, добавьте в чашку эспрессо и посыпьте корицей.",
        "изображение": "images/latte.jpg"
    },
    "Эспрессо": {
        "Рецепт": "Для приготовления эспрессо нужно пропустить горячую воду под давлением через мелко измельчённый кофе, используя эспрессо-машину.",
        "изображение": "images/simplecoffee.jpg"
    },
    "Мокко": {
        "Рецепт": "Для приготовления мокко нужно соединить эспрессо, тёплое молоко и шоколадный сироп, а затем взбить смесь до образования пены.",
        "изображение": "images/mokko.jpg"
    }
}

random_router = Router()


@random_router.message(Command('random'))
async def send_random_recipe(message: types.Message):
    random_recipe_name = choice(list(recipes.keys()))
    random_recipe = recipes[random_recipe_name]

    random_recipe_image = types.FSInputFile(random_recipe["изображение"])
    await message.answer_photo(
        photo=random_recipe_image,
        caption=f"Вот случайный рецепт {random_recipe_name}: {random_recipe['Рецепт']}")
