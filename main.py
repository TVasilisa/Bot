import asyncio
from random import choice
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import dotenv_values
import logging


token = dotenv_values(".env")['BOT_TOKEN']
bot = Bot(token=token)
dp = Dispatcher()

names = ['Игнат', 'Степан', 'Анатолий', 'Азамат', 'Венера', 'Евпатий', 'Стив']

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    if name is not None:
        await message.answer(f"Привет, {name}")
    else:
        await message.answer(f'Привет, пользователь!')

@dp.message(Command('myinfo'))
async def myinfo_handler(message: types.Message):
    usersid = message.from_user.id
    firstname = message.from_user.first_name
    username = message.from_user.username
    if username is not None:
        await message.answer(
            f'Хмм..Посмотрим, какая информация о тебе у меня есть. Твой id:{usersid}, твоё имя {firstname}, имя пользователя {username}')
    else:
        await message.answer(
            f'Хмм..Посмотрим, какая информация о тебе у меня есть. Твой id:{usersid}, твоё имя {firstname}, у тебя нет имени пользователя.')

@dp.message(Command('random'))
async def random_handler(message: types.Message):
    random_name = choice(names)
    await message.answer(f'Случайное имя из списка: {random_name}')



@dp.message()
async def echo_handler(message: types.message):
    txt = message.text
    await message.answer(txt)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())