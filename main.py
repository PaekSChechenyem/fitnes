from aiogram import Dispatcher
from auth import bot
import asyncio
import payments_router 
import quiz_router
import users_router
import callback_router
from db import database
from filters import PrivateFilter

async def main():
    await database.init_db()
    dp = Dispatcher()
    dp.message.filter(PrivateFilter())
    dp.include_routers(payments_router.router,
                       quiz_router.router,
                       users_router.router,
                       callback_router.router)
    await dp.start_polling(bot)

asyncio.run(main())


