import telebot
from telebot import types

import time

token = '2085419627:AAFaAvnPisevlhyEfpG1m8rA8kmYRlKnXG4'
bot = telebot.TeleBot(token=token, parse_mode=None)

@bot.message_handler(commands=['start'])
def start(message):
    text = '''Привет!\n Рада, что ты решил(а) провести четверг с пользой и сделал(а) первый шаг на пути к новой жизни.\n\nДля регистрации на открытый вебинар в zoom «Как новичку или действующему поставщику выйти на миллион без рисков» остался один шаг:\n\nНапиши <b> корректно свой номер телефона </b> в ответ на это сообщение.\n\nСразу после тебе придёт ссылка на канал вебинара.
            '''
    bot.send_photo(message.chat.id, open(r'photoswb\Frame 47 (1).png', 'rb'), caption=text, parse_mode='HTML')
    phone(message)
    
def phone (message):
    keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True, one_time_keyboard=True)
    button_phone = types.KeyboardButton(text = "Отправить номер", request_contact = True)
    keyboard.add(button_phone)
