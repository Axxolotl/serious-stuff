# импорт библиотек для написания бота
import telebot
from telebot import types # для указание типов

# пандас для работы с таблицей пользователей (в дальнейшем возможна замена на json)
import pandas as pd
# считываем таблицу с данными юзеров
df = pd.read_csv('DB_RSUH_users.csv').drop('Unnamed: 0', axis=1)

##################################################################################
# создаем сущность бота
token = '2085419627:AAFaAvnPisevlhyEfpG1m8rA8kmYRlKnXG4'
bot = telebot.TeleBot(token, parse_mode=None)

# реакция бота на /start
@bot.message_handler(commands=['start'])
def start(message):
    # создаем запись в таблице и записываем в колонку id ник пользователя в тг (нужно потом сделать проверку на существование пользователя в базе)
    df.loc[len(df)-1] = [message.from_user.username, '', '', '']
    
    # создаем кнопки для ввода стартовой информации
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Ввести форму обучения")
    btn2 = types.KeyboardButton("Ввести курс")
    btn3= types.KeyboardButton('Ввести название специальности')
    markup.add(btn1, btn2, btn3)
    
    # приветственное сообщение
    bot.send_photo(message.chat.id, "https://i.pinimg.com/originals/ae/18/b0/ae18b0d2525ea57e7c903960f6d84c4a.jpg",  reply_markup=markup)

# функция - обработчик кнопок
@bot.message_handler(content_types=['text'])
def enter_info(message):
    
    # ввод формы обучения
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
        # отправляем форму обучения на запись в таблицу (мб можно через лямбда функцию записать??)
        bot.register_next_step_handler(dict_form[int(message)], get_form)
        
     # ввод курса
    elif message.text == 'Ввести курс':
        bot.send_message(message.chat.id, "Отправь мне цифру своего курса")
        # отправляем курс на проверку и запись
        bot.register_next_step_handler(message, user_faculty)
        
     # ввод факультета (сделать ту штуку с парсером)
    elif message.text == 'Ввести название специальности':
        bot.send_message(message.chat.id, 'Отправь мне свою специальность')
        # отправляем факультет на запись
        bot.register_next_step_handler(message, user_speciality)
        
        
####################################################### ЗАПИСИ ПЕРЕМЕННЫХ В БАЗУ ДАННЫХ ###############################################################
# форма обучения
    def get_form(message):
        form_edu = message.text
        df.loc[df[df['id']==message.from_user.username].index, 'education_form'] = form_edu
# курс
    def user_faculty(message):
        if int(message.text) in range(1,7): 
            faculty = message.text
            bot.send_message(message.chat.id, faculty)
            df.loc[df[df['id']==message.from_user.username].index, 'faculty'] = faculty
            
# специальность       
    def user_speciality(message):
        speciality = message.text
        bot.send_message(message.chat.id, speciality)
        df.loc[df[df['id']==message.from_user.username].index, 'speciality'] = speciality
