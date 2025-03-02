from aiogram import Router, F
from aiogram.types import PreCheckoutQuery, Message, LabeledPrice
from db import database
from filters import PaidFilter
from auth import payments_token, bot
from db import database

router = Router()

price = LabeledPrice(label='Доступ к функциям бота', amount=10000)

@router.message(F.successful_payment)
async def handler(msg: Message):
    await bot.delete_message(chat_id=msg.from_user.id,
                             message_id=await database.get_offer_msg_id(msg.from_user.id))
    await msg.answer('Доступ оплачен! Теперь введи свой возраст (просто число)')

@router.message(PaidFilter())
async def msg_handler(msg: Message):
    offer_msg = await msg.answer_invoice(
        title='Доступ',
        description='Возможность пользоваться ботом',
        provider_token=payments_token,
        currency='rub',
        payload='some-invoice-payload-for-our-internal-use',
        prices=[price])
    await database.update_offer(msg.from_user.id, offer_msg.message_id)

@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

