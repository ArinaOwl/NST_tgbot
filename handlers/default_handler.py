from aiogram import types
from misc import dp


@dp.message_handler()
async def all_other_messages(msg):
    await msg.answer("Я тебя не понимаю. \nВоспользуйся /help.")
