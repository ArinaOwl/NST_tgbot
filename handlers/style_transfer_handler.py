from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from misc import dp, bot
from model import NST_Model as model

import asyncio

class StyleTransfer(StatesGroup):
    waiting_for_style_img = State()
    waiting_for_content_img = State()
    
@dp.message_handler(commands=['style_transfer'], state='*')
async def style_transfer_step_1(msg):
    await msg.answer("Запущен перенос стиля.\nДля отмены отправь команду /cancel.")
    await msg.answer("Отправь картинку стиля.")
    await StyleTransfer.waiting_for_style_img.set()
    
@dp.message_handler(commands=['cancel'], state='*')
async def process_cancel_command(msg, state: FSMContext):
    await msg.answer("Процесс переноса стиля отменен. \nДля запуска отправь /style_transfer.")
    await state.finish()

@dp.message_handler(state=StyleTransfer.waiting_for_style_img, content_types=['photo'])
async def style_transfer_step_2(msg, state: FSMContext):
    await msg.photo[-1].download('images/style.jpg')
    await msg.answer("Отправь картинку для переноса стиля.")
    await StyleTransfer.waiting_for_content_img.set()

@dp.message_handler(state=StyleTransfer.waiting_for_style_img)
async def style_transfer_step_2(msg, state: FSMContext):
    await msg.answer("Что-то пошло не так. Попробуй отправить картинку стиля снова или отправь для отмены /cancel.")
    
@dp.message_handler(state=StyleTransfer.waiting_for_content_img, content_types=['photo'])
async def style_transfer_step_3(msg, state: FSMContext):
    await msg.photo[-1].download('images/content.jpg')
    await msg.answer("Начинаю обработку. На это потребуется некоторое время.")
    await model(open('images/style.jpg', 'rb'), open('images/content.jpg', 'rb'), open('images/content.jpg', 'rb')).run_style_transfer()
    await msg.answer("Обработка завершена.")
    await bot.send_photo(msg.from_user.id, open('images/output.jpg', 'rb'))
    await msg.answer("Для запуска переноса стиля отправь /style_transfer.")
    await state.finish()

@dp.message_handler(state=StyleTransfer.waiting_for_content_img)
async def style_transfer_step_3(msg, state: FSMContext):
    await msg.answer("Что-то пошло не так. Попробуй отправить картинку для переноса стиля снова или отправь для отмены /cancel.")
