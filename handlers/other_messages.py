from aiogram import Router, types
from aiogram.filters import Command

other_router = Router()


@other_router.message()
async def echo_handler(message: types.Message):
    await message.answer("Я вас не понимаю")
