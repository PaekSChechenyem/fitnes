from aiogram.filters import BaseFilter
from aiogram.types import Message
from db import database

class PaidFilter(BaseFilter):  
    async def __call__(self, msg: Message) -> bool: 
        return await database.check_paid(msg.from_user.id) == False
    
class PrivateFilter(BaseFilter):  
    async def __call__(self, msg: Message) -> bool: 
        return msg.chat.type == 'private'
    
class BufferFilter(BaseFilter):  
    async def __call__(self, msg: Message) -> bool: 
        return await database.check_buffer(msg.from_user.id) == False
    
class UsersFilter(BaseFilter):  
    async def __call__(self, msg: Message) -> bool: 
        return await database.check_buffer(msg.from_user.id) == True
    
class StateFilter(BaseFilter):  
    def __init__(self, state: int):
        self.state = state
    async def __call__(self, msg: Message) -> bool: 
        return await database.get_buffer_state(msg.from_user.id) == self.state