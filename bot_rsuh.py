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
    if message.text == 'Ввести форму обучения':
        dict_form = {
            1: 'Дневная',
            2: "Вечерняя",
            3: "Заочная",
            4: "Второе образование",
            5: "Магистратура",
            6: "Аспирантура",
            7: "Дистанционное"
        }
        bot.send_message(message.chat.id, text='\n'.join([str(i) + '. ' + j for i,j in dict_form.items()]))
        bot.send_message(message.chat.id, text='Введите цифру, соответствующую Вашей форме')
        bot.register_next_step_handler(message, get_form)
     elif message.text == 'Ввести курс':
        bot.send_message(message.chat.id, "Отправь мне цифру своего курса")
            bot.register_next_step_handler(message, user_faculty)
     elif message.text == 'Ввести название специальности':
        bot.send_message(message.chat.id, 'Отправь мне свою специальность')
        bot.register_next_step_handler(message, user_speciality)
        
        
        
        
    def get_form(message):
        form_edu = message.text
        bot.send_message(message.chat.id, text=form_edu)
        
    def user_faculty(message):
        if int(message.text) in range(1,7): 
            faculty = message.text
            bot.send_message(message.chat.id, faculty)
       
    def user_speciality(message):
        speciality = message.text
        bot.send_message(message.chat.id, speciality)
