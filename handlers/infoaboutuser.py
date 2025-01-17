from aiogram import Router, types
from aiogram.filters import Command

myinfo_router = Router()


@myinfo_router.message(Command('myinfo'))
async def myinfo_handler(message: types.Message):
    usersid = message.from_user.id
    firstname = message.from_user.first_name
    username = message.from_user.username
    if username is not None:
        await message.answer(
            f'Хмм.. Посмотрим, какая информация о тебе у меня есть. Твой id:{usersid}, твоё имя {firstname}, имя пользователя {username}')
    else:
        await message.answer(
            f'Хмм.. Посмотрим, какая информация о тебе у меня есть. Твой id:{usersid}, твоё имя {firstname}, у тебя нет имени пользователя.')
