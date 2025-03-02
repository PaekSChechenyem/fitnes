from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

kb=[[KeyboardButton(text='М'), KeyboardButton(text='Ж')],
    [KeyboardButton(text='Назад')]]
sex_back=ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

kb=[[KeyboardButton(text='Назад')]]
back=ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

kb=[[KeyboardButton(text='Пропустить')]]
skip=ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

kb=[[KeyboardButton(text='Пропустить')], 
    [KeyboardButton(text='Назад')]]
skip_back=ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

kb = [[InlineKeyboardButton(text='Сгенерировать тренировку', callback_data='new')]]
root = InlineKeyboardMarkup(inline_keyboard=kb)

kb = [[InlineKeyboardButton(text='Сушка', callback_data='Сушка')],
      [InlineKeyboardButton(text='Массанабор', callback_data='Массанабор')],
      [InlineKeyboardButton(text='Поддержание формы', callback_data='Поддержание формы')],
      [InlineKeyboardButton(text='Назад', callback_data='back')]]
select_target = InlineKeyboardMarkup(inline_keyboard=kb)

kb = [[InlineKeyboardButton(text='Пауэрлифтинг', callback_data='Пауэрлифтинг')],
      [InlineKeyboardButton(text='Бодибилдинг', callback_data='Бодибилдинг')],
      [InlineKeyboardButton(text='Турник/воркаут', callback_data='Турник/воркаут')],
      [InlineKeyboardButton(text='Общая тренировка', callback_data='Общая тренировка')],
      [InlineKeyboardButton(text='Назад', callback_data='back')]]
select_type = InlineKeyboardMarkup(inline_keyboard=kb)

kb = [[InlineKeyboardButton(text='Полное тело', callback_data='Полное тело')],
      [InlineKeyboardButton(text='Отдельная группа мышц', callback_data='Отдельная группа мышц')],
      [InlineKeyboardButton(text='Сплит', callback_data='Сплит')],
      [InlineKeyboardButton(text='Назад', callback_data='back')]]
select_format = InlineKeyboardMarkup(inline_keyboard=kb)

kb = [[InlineKeyboardButton(text='Легкая', callback_data='Легкая')],
      [InlineKeyboardButton(text='Средняя', callback_data='Средняя')],
      [InlineKeyboardButton(text='Тяжелая', callback_data='Тяжелая')],
      [InlineKeyboardButton(text='Назад', callback_data='back')]]
select_load = InlineKeyboardMarkup(inline_keyboard=kb)

kb = [[InlineKeyboardButton(text='Грудь + плечи', callback_data='Грудь + плечи')],
      [InlineKeyboardButton(text='Спина + бицепс', callback_data='Спина + бицепс')],
      [InlineKeyboardButton(text='Ноги + трицепс', callback_data='Ноги + трицепс')],
      [InlineKeyboardButton(text='Назад', callback_data='back')]]
select_split = InlineKeyboardMarkup(inline_keyboard=kb)

kb = [[InlineKeyboardButton(text='Грудь', callback_data='Грудь')], 
      [InlineKeyboardButton(text='Спина', callback_data='Спина')],
      [InlineKeyboardButton(text='Плечи', callback_data='Плечи')],
      [InlineKeyboardButton(text='Бицепс', callback_data='Бицепс')],
      [InlineKeyboardButton(text='Трицепс', callback_data='Трицепс')],
      [InlineKeyboardButton(text='Ноги', callback_data='Ноги')],
      [InlineKeyboardButton(text='Пресс', callback_data='Пресс')],
      [InlineKeyboardButton(text='Назад', callback_data='back')]]
select_group = InlineKeyboardMarkup(inline_keyboard=kb)

kb = [[InlineKeyboardButton(text='На месяц', callback_data='На месяц')],
      [InlineKeyboardButton(text='На неделю', callback_data='На неделю')],
      [InlineKeyboardButton(text='Разовая (одна тренировка)', callback_data='Разовая (одна тренировка)')],
      [InlineKeyboardButton(text='Назад', callback_data='back')]]
select_period = InlineKeyboardMarkup(inline_keyboard=kb)

kb = [[InlineKeyboardButton(text='Сгенерировать', callback_data='Сгенерировать')],
      [InlineKeyboardButton(text='Назад', callback_data='back')]]
gen = InlineKeyboardMarkup(inline_keyboard=kb)