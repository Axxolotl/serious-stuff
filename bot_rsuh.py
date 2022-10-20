import telebot
from telebot import types # для указание типов

token = '2085419627:AAFaAvnPisevlhyEfpG1m8rA8kmYRlKnXG4'
bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Ввести форму обучения")
    btn2 = types.KeyboardButton("Ввести курс")
    btn3= types.KeyboardButton('Ввести название специальности')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет!",  reply_markup=markup)

# пишем эту функцию
@bot.message_handler(content_types=['text'])
def enter_info(message):
