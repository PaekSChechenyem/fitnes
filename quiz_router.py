from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from filters import StateFilter, BufferFilter
from db import database
from keyboards import *
from auth import bot

#роутер для опроса пользователей и сохранения их данных
router = Router()
router.message.filter(BufferFilter()) #пропускает тех, кто уже оплатил доступ, но еще не прошел опрос

states = ['yob', 'sex', 'weight', 'height', 'health', 'training', 'food']

async def create_user(user_id):
    await database.from_b2u(user_id)
    await bot.send_message(chat_id=user_id, text='Данные сохранены!', reply_markup=ReplyKeyboardRemove())
    menu_msg = await bot.send_message(chat_id=user_id, text='теперь ты можешь юзать менюшку',
                           reply_markup=root)
    await database.create_menu(user_id, menu_msg.message_id)

@router.message(F.text == 'Пропустить')
async def handler(msg: Message):
    state = await database.get_buffer_state(msg.from_user.id)
    if state != 'food':
        await database.update_buffer(msg.from_user.id, state, '-1')
        next_state = states[states.index(state) + 1]
        await database.set_buffer_state(msg.from_user.id, next_state)
        if next_state == 'food':
            await msg.answer('питание: пищевые предпочтения (вегетарианец, \
веган, безглютеновая диета и т.д.), аллергии на продукты', reply_markup=skip_back)
        if next_state == 'training':
            await msg.answer('уровень физической подготовки (опыт в спорте,\
    выносливость, общая оценка спортивной формы)', reply_markup=skip_back)
    else:
        await database.update_buffer(msg.from_user.id, 'food', '-1')
        await create_user(msg.from_user.id)

@router.message(F.text == 'Назад')
async def handler(msg: Message):
    state = await database.get_buffer_state(msg.from_user.id)
    back_to = states[states.index(state) - 1]
    await database.set_buffer_state(msg.from_user.id, back_to)
    if back_to == 'yob':
        await msg.answer('Введи свой возраст (числом)', reply_markup=ReplyKeyboardRemove())
    if back_to == 'sex':
        await msg.answer('Выбери свой пол', reply_markup=sex_back)
    if back_to == 'weight':
        await msg.answer('Введи свой вес в кг (числом)', reply_markup=back)
    if back_to == 'height':
        await msg.answer('Введи свой рост в см(числом)', reply_markup=back)
    if back_to == 'health':
        await msg.answer('наличие хронических заболеваний (например,\
 диабет, гипертония), ограничения по здоровью (например, проблемы с суставами, сердце), травмы, уровень стресса', reply_markup=back)
    if back_to == 'training':
        await msg.answer('уровень физической подготовки (опыт в спорте,\
 выносливость, общая оценка спортивной формы)', reply_markup=back)


@router.message(StateFilter('yob'))
async def handler(msg: Message):
    if msg.text and msg.text.isdigit() and int(msg.text)<100:
        await database.update_buffer(msg.from_user.id, 'yob', 2025-int(msg.text))
        await database.set_buffer_state(msg.from_user.id, 'sex')
        await msg.answer('Выбери свой пол', reply_markup=sex_back)
    else:
        await msg.answer('Ты ввел некорректное значение')

@router.message(StateFilter('sex'))
async def handler(msg: Message):
    if msg.text and msg.text in ['М', 'Ж']:
        await database.update_buffer(msg.from_user.id, 'sex', msg.text)
        await database.set_buffer_state(msg.from_user.id, 'weight')
        await msg.answer('Введи свой вес в кг (числом)', reply_markup=back)
    else:
        await msg.answer('Ты ввел некорректное значение', reply_markup=back)

@router.message(StateFilter('weight'))
async def handler(msg: Message):
    if msg.text and msg.text.isdigit() and 20<int(msg.text)<400:
        await database.update_buffer(msg.from_user.id, 'weight', msg.text)
        await database.set_buffer_state(msg.from_user.id, 'height')
        await msg.answer('Введи свой рост в см(числом)')
    else:
        await msg.answer('Ты ввел некорректное значение', reply_markup=back)

@router.message(StateFilter('height'))
async def handler(msg: Message):
    if msg.text and msg.text.isdigit() and 80<int(msg.text)<250:
        await database.update_buffer(msg.from_user.id, 'height', msg.text)
        await database.set_buffer_state(msg.from_user.id, 'health')
        await msg.answer('наличие хронических заболеваний (например,\
 диабет, гипертония), ограничения по здоровью (например, проблемы с суставами, сердце), травмы, уровень стресса', reply_markup=skip_back)
    else:
        await msg.answer('Ты ввел некорректное значение', reply_markup=back)

@router.message(StateFilter('health'))
async def handler(msg: Message):
    if msg.text:
        await database.update_buffer(msg.from_user.id, 'health', msg.text)
        await database.set_buffer_state(msg.from_user.id, 'training')
        await msg.answer('уровень физической подготовки (опыт в спорте,\
 выносливость, общая оценка спортивной формы)', reply_markup=skip_back)
    else:
        await msg.answer('Ты ввел некорректное значение', reply_markup=back)

@router.message(StateFilter('training'))
async def handler(msg: Message):
    if msg.text:
        await database.update_buffer(msg.from_user.id, 'training', msg.text)
        await database.set_buffer_state(msg.from_user.id, 'food')
        await msg.answer('питание: пищевые предпочтения (вегетарианец, \
веган, безглютеновая диета и т.д.), аллергии на продукты', reply_markup=skip_back)
    else:
        await msg.answer('Ты ввел некорректное значение', reply_markup=back)

@router.message(StateFilter('food'))
async def handler(msg: Message):
    if msg.text:
        await database.update_buffer(msg.from_user.id, 'food', msg.text)
        await create_user(msg.from_user.id)
    else:
        await msg.answer('Ты ввел некорректное значение', reply_markup=back)

