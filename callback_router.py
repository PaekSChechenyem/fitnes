from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from keyboards import *
from db import *
from auth import bot
from surwey import sur
from gpt import generate_answer
from create_pdf import save_pdf
import os

router = Router()

#генерация плана тренировок и отправка файла
@router.callback_query(F.data == 'Сгенерировать')
async def cb_handler(callback: CallbackQuery):
    await callback.answer()
    await bot.send_message(chat_id=callback.from_user.id, text='Генерирую план...')
    prompt = await database.get_prompt(callback.from_user.id) #формирование промта для запроса из данных пользователя и вида тренировки
    text = await generate_answer(prompt) 
    await save_pdf(text.choices[0].message.content, callback.from_user.id)
    pdf = FSInputFile(f'{callback.from_user.id}.pdf')
    await bot.send_document(callback.from_user.id, pdf)
    os.remove(f'{callback.from_user.id}.pdf')
    await database.zero_menu(callback.from_user.id) #сброс введенных характеристик тренировки
    await sur.resend_menu(callback.from_user.id) #переотправка меню после отправки файла с планом тренировки

#возвращение к выбору предыдущего параметра тренировки (или возвращение в основное меню)
@router.callback_query(F.data == 'back')
async def cb_handler(callback: CallbackQuery):
    await callback.answer()
    await sur.back(callback.from_user.id, callback)

#переход к последовательному выбору параметров тренировки
@router.callback_query(F.data == 'new')
async def cb_handler(callback: CallbackQuery):
    await callback.answer()
    await sur.start(callback.from_user.id, callback)

#переход к выбору следующего параметра тренировки (или переход к предложению сгенерировать тренировку по введенным параметрам)
@router.callback_query()
async def cb_handler(callback: CallbackQuery):
    await callback.answer()
    await sur.next_step(callback.from_user.id, callback)