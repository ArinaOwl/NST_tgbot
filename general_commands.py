from aiogram import types
from misc import dp

@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    await msg.answer("Привет! Я, ImageBot, умею переносить стиль одной картинки на другую. \nДля общения со мной используй данные команды: \n/help - получить инструкции \n/style_transfer - начать обработку изображений \n/cancel - отменить все.")
    
@dp.message_handler(commands=['help'])
async def process_help_command(msg: types.Message):
    await msg.answer("Для общения со мной используй данные команды: \n/help - получить инструкции \n/style_transfer - начать обработку изображений \n/cancel - отменить все.")
