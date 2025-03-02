from keyboards import *
from db import database
from auth import bot

#объект, с помощью которого происходит редактирование меню на этапе выбора пользователем характеристик тренировки
class Surwey():

    states_arr = ['default', 'target', 'type', 'load', 'period']
    states = {
        'default': ['Что нужно сделать?', root],
        'target': ['Выбери цель тренировки', select_target],
        'type': ['Выбери тип тренировки', select_type],
        'format': ['Выбери формат тренировки', select_format],
        'mgroup': ['Выбери группу мышц', select_group],
        'split': ['Выбери группу мышц', select_split],
        'load': ['Выбери уровень нагрузки', select_load],
        'period': ['Выбери период тренировки', select_period]
    }

    async def next_state(self, current_state, callback_data):

        #с помощью словаря определяем, к выбору какого параметра перейти далее, учитывая название и значение выбранного параметра
        transitions = {
            ('target', callback_data): 'type',
            ('type', 'Бодибилдинг'): 'format',
            ('type', callback_data if callback_data != 'Бодибилдинг' else 0): 'load',
            ('format', 'Отдельная группа мышц'): 'mgroup',
            ('format', 'Сплит'): 'split',
            ('format', 'Полное тело'): 'load',
            ('mgroup', callback_data): 'load',
            ('split', callback_data): 'load',
            ('load', callback_data): 'period',
            ('period', callback_data): 'gen'
        }
        return transitions[(current_state, callback_data)]

    async def resend_menu(self, user_id):

        old_menu_msg_id = await database.get_menu_msg_id(user_id)
        state = await database.get_menu_state(user_id)
        form = await database.get_form(user_id)
        new_menu = await bot.send_message(chat_id=user_id,
                                          text=form+self.states[state][0],
                                          reply_markup=self.states[state][1],
                                          parse_mode='HTML')
        await bot.delete_message(chat_id=user_id,
                                 message_id=old_menu_msg_id)
        await database.update_menu(user_id, 'msg_id', new_menu.message_id)
    
    async def start(self, user_id, callback):

        
        await database.set_menu_state(user_id, 'target')
        form = await database.get_form(user_id)
        await bot.edit_message_text(text=form+'Выбери цель тренировки:', 
                                    reply_markup=select_target,
                                    chat_id=user_id,
                                    message_id=callback.message.message_id,
                                    parse_mode='HTML')

    async def next_step(self, user_id, callback):

        state = await database.get_menu_state(user_id)
        if state == 'period':
            await database.update_menu(user_id, state, callback.data)
            form = await database.get_form(user_id)
            await bot.edit_message_text(text=form+'генерируем?', 
                                        reply_markup=gen,
                                        chat_id=user_id,
                                        message_id=callback.message.message_id,
                                        parse_mode='HTML')
        else:
            new_state = await self.next_state(state, callback.data)
            await database.update_menu(user_id, state, callback.data)
            await database.set_menu_state(user_id, new_state)
            form = await database.get_form(user_id)
            await bot.edit_message_text(text=form+self.states[new_state][0], 
                                        reply_markup=self.states[new_state][1],
                                        chat_id=user_id,
                                        message_id=callback.message.message_id,
                                        parse_mode='HTML')
    
    async def back(self, user_id, callback):
        
        format = await database.get_from_menus(callback.from_user.id, 'format')
        
        #с помощью словаря определяем, к выбору какого параметра вернуться, учитывая название текущего параметра и значение format 
        transitions = {
            ('period', format): 'load',
            ('load', '-1'): 'type',
            ('load', 'Полное тело'): 'format',
            ('load', 'Отдельная группа мышц'): 'mgroup',
            ('load', 'Сплит'): 'split',
            ('split', 'Сплит'): 'format',
            ('mgroup', 'Отдельная группа мышц'): 'format',
            ('format', format): 'type',
            ('type', format): 'target', 
            ('target', format): 'default'
        }
        
        current_state = await database.get_menu_state(callback.from_user.id)
        prev_state = transitions[(current_state, format)]
        await database.set_menu_state(callback.from_user.id, prev_state)
        if prev_state != 'default':
            await database.update_menu(user_id, prev_state, '-1')
        form = await database.get_form(user_id)
        await bot.edit_message_text(text=form+self.states[prev_state][0], 
                                    reply_markup=self.states[prev_state][1],
                                    chat_id=user_id,
                                    message_id=callback.message.message_id,
                                    parse_mode='HTML')

sur = Surwey()