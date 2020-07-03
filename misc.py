import logging
from aiogram import Bot, Dispatcher
from config import TOKEN, MEMORY_STORAGE

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage = MEMORY_STORAGE)
logging.basicConfig(level=logging.INFO)
