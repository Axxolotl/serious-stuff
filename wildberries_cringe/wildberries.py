import telebot
from telebot import types

import time

token = '2085419627:AAFaAvnPisevlhyEfpG1m8rA8kmYRlKnXG4'
bot = telebot.TeleBot(token=token, parse_mode=None)

@bot.message_handler(commands=['start'])
def start(message):
    text = '''Привет!\n Рада, что ты решил(а) провести четверг с пользой и сделал(а) первый шаг на пути к новой жизни.\n\n
    Для регистрации на открытый вебинар в zoom «Как новичку или действующему поставщику выйти на миллион без рисков» 
    остался один шаг:\n\nНапиши <b> корректно свой номер телефона </b> в ответ на это сообщение.\n\n
    Сразу после тебе придёт ссылка на канал вебинара.
            '''
    bot.send_message(message.chat.id, text, parse_mode="HTML")
