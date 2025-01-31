from aiogram import Router, F, types

punish_router = Router()
punish_router.message.filter(F.chat.type != 'private')

BAD_WORDS = ('дурак', 'чёрт', 'тупой')


@punish_router.message(F.text)
async def check_bad_words(message: types.Message):
    for word in BAD_WORDS:
        if word in message.text.lower():
            await message.answer("Отвратительно себя ведёшь")
            await message.delete()
            await message.chat.ban(message.from_user.id)
            return


