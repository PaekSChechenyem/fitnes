from aiogram import Router
from aiogram.types import Message
from filters import UsersFilter
from surwey import sur

router = Router()
router.message.filter(UsersFilter())

@router.message()
async def handler(msg: Message):
    await sur.resend_menu(msg.from_user.id) #удаление и переотправка меню каждый раз, когда пользователь что-то пишет