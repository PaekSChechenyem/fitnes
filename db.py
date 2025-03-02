import aiosqlite
from auth import bot

#В buffer хранятся данные пользователей на этапе опроса, после завершения опроса данные навсегде переносятся в users
class Database():
    async def init_db(self):
        self.db = await aiosqlite.connect('fitnes.db')
        await self.db.execute('CREATE TABLE IF NOT EXISTS payment_offers (user_id int, msg_id int)')
        await self.db.execute('CREATE TABLE IF NOT EXISTS buffer (\
                              user_id int,\
                              yob int,\
                              sex text,\
                              weight int,\
                              height int,\
                              health text,\
                              training text,\
                              food text,\
                              state text)')
        await self.db.execute('CREATE TABLE IF NOT EXISTS users (\
                              user_id int,\
                              yob int,\
                              sex text,\
                              weight int,\
                              height int,\
                              health text,\
                              training text,\
                              food text)')
        await self.db.execute('CREATE TABLE IF NOT EXISTS menus (\
                              user_id int,\
                              msg_id int,\
                              state text,\
\
                              target text,\
                              type text,\
                              format text,\
                              mgroup text,\
                              split text,\
                              load text,\
                              period text)')
        
    async def create_menu(self, user_id, msg_id):
        await self.db.execute('INSERT INTO menus VALUES (?, ?, "default", "-1", "-1", "-1", "-1", "-1", "-1", "-1")', (user_id, msg_id))
        await self.db.commit()

    async def check_paid(self, user_id):
        user_buffer = await self.db.execute_fetchall('SELECT user_id FROM buffer WHERE user_id = ?', (user_id,))
        user = await self.db.execute_fetchall('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
        if user_buffer != [] or user != []:
            return True
        else:
            return False
        
    async def check_buffer(self, user_id):
        user = await self.db.execute_fetchall('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
        if user != []:
            return True
        else:
            return False
        
    async def update_offer(self, user_id, msg_id): 
        offer = await self.db.execute_fetchall('SELECT user_id FROM payment_offers WHERE user_id = ?', (user_id,))
        if offer == []:
            await self.db.execute('INSERT INTO payment_offers VALUES (?, ?)', (user_id, msg_id))
            await self.db.commit()
        else:
            old_msg_id = await self.db.execute_fetchall('SELECT msg_id FROM payment_offers WHERE user_id = ?', (user_id,))
            old_msg_id = old_msg_id[0][0]
            await self.db.execute('UPDATE payment_offers SET msg_id = ? WHERE user_id = ?', (msg_id, user_id))
            await self.db.commit()
            await bot.delete_message(chat_id=user_id,
                                     message_id=old_msg_id)
            
    async def add_user_buffer(self, user_id):
        await self.db.execute('INSERT INTO buffer VALUES (?, -1, "-1", -1, -1, "-1", "-1", "-1", "yob")', (user_id,))
        await self.db.commit()

    async def get_offer_msg_id(self, user_id):
        offer_msg_id = await self.db.execute_fetchall('SELECT msg_id FROM payment_offers WHERE user_id = ?', (user_id,))
        offer_msg_id = offer_msg_id[0][0]
        await self.db.execute('DELETE FROM payment_offers WHERE user_id = ?', (user_id,))
        await self.db.commit()
        await self.add_user_buffer(user_id)
        return offer_msg_id
    
    async def get_buffer_state(self, user_id):
        state = await self.db.execute_fetchall('SELECT state FROM buffer WHERE user_id = ?', (user_id,))
        return state[0][0]

    async def set_buffer_state(self, user_id, state):
        await self.db.execute('UPDATE buffer SET state = ? WHERE user_id = ?', (state, user_id))
        await self.db.commit()

    async def update_buffer(self, user_id, field, value):
        await self.db.execute(f'UPDATE buffer SET {field} = ? WHERE user_id = ?', (value, user_id))
        await self.db.commit()

    async def from_b2u(self, user_id):
        user = await self.db.execute_fetchall('SELECT * FROM buffer WHERE user_id = ?', (user_id,))
        user = user[0]
        await self.db.execute('DELETE FROM buffer WHERE user_id = ?', (user_id,))
        await self.db.commit()
        await self.db.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user[0],user[1],user[2],user[3],user[4],user[5],user[6], user[7]))
        await self.db.commit()
    
    async def update_menu(self, user_id, field, value):
        await self.db.execute(f'UPDATE menus SET {field} = ? WHERE user_id = ?', (value, user_id))
        await self.db.commit()

    async def get_menu_state(self, user_id):
        state = await self.db.execute_fetchall('SELECT state FROM menus WHERE user_id = ?', (user_id,))
        return state[0][0]
    
    async def set_menu_state(self, user_id, state):
        await self.db.execute(f'UPDATE menus SET state = ? WHERE user_id = ?', (state, user_id))
        await self.db.commit()

    async def reload_menu(self, user_id, msg_id):
        await self.db.execute('DELETE FROM menus WHERE user_id = ?', (user_id,))
        await self.db.commit()
        await self.db.execute('INSERT INTO menus VALUES (?, ?, "default", "-1", "-1", "-1", "-1", "-1", "-1")', (user_id, msg_id))
        await self.db.commit()

    async def get_menu_msg_id(self, user_id):
        msg_id = await self.db.execute_fetchall('SELECT msg_id FROM menus WHERE user_id = ?', (user_id,))
        return msg_id[0][0]
        
    async def get_from_menus(self, user_id, field):
        value = await self.db.execute_fetchall(f'SELECT {field} FROM menus WHERE user_id = ?', (user_id,))
        return value[0][0]
    
    async def zero_menu(self, user_id):
        await self.db.execute('UPDATE menus SET state = "default",\
                              target = "-1",\
                              type = "-1",\
                              format = "-1",\
                              mgroup = "-1",\
                              split = "-1",\
                              load = "-1",\
                              period = "-1" WHERE user_id = ?', (user_id,))
        await self.db.commit()

    async def get_form(self, user_id):
        values = await self.db.execute_fetchall('SELECT target, type, format, mgroup, \
                                                split, load, period FROM menus WHERE user_id = ?', (user_id,))
        values = values[0]
        fields = ['Цель: ','Тип: ','Формат: ','Группа мышц: ','Группы мышц: ','Нагрузка: ','Период: ']
        text = ''
        for i in values:
            if i != '-1':
                text += f'<b>{fields[values.index(i)]}</b>\n{i}\n\n'
        return text

    async def get_prompt(self, user_id):
        person = await self.db.execute_fetchall('SELECT yob int,\
                              sex text,\
                              weight int,\
                              health text,\
                              training text FROM users WHERE user_id = ?', (user_id,))
        fields = ['возраст: ','пол: ','вес: ','описание состояния здоровья: ','описание физической подготовки: ']
        text1 = ''
        for i in person[0]:
            if i not in ['-1', -1]:
                text1 += fields[person[0].index(i)]+str(i)+', '
        text1 = 'Описание клиента: '+text1[:-2]+'.'

        values = await self.db.execute_fetchall('SELECT target, type, format, mgroup, \
                                                split, load, period FROM menus WHERE user_id = ?', (user_id,))
        values = values[0]
        fields = ['цель: ','тип: ','формат: ','группа мышц: ','группы мышц: ','нагрузка: ','период: ']
        text2 = ''
        for i in values:
            if i != '-1':
                text2 += f'{fields[values.index(i)]}{i}, '
        text2 = 'Характеристики тренировки: '+text2[:-2]+'.'
        prompt = 'Ты - специалист по фитнесу. Тебе нужно составить индивидуализированный план тренировки/тренировок для клиента. '\
+text1+' '+text2+' В своем ответе обращайся к клиенту во втором лице. План обязательно должен учитывать описание клиента. \
Будь максимально краток, все твои пояснения должны касаться только тех аспектов составленного плана, на которые повлияло описание клиента. Обязательно\
должно быть несколько пояснений к каким-то частям плана, эти пояснения должны давать понять клиенту, что план является индивидуализированным и рассчитан\
на именно его параметры.'

        return prompt

database = Database()