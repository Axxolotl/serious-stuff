import telebot
from telebot import types

import re
import RSUH_parsing_raspis
from RSUH_parsing_raspis import create_table
from RSUH_parsing_raspis import parse_rsuh

import json
with open('специальности.json', 'r', encoding='utf-8') as file:
    specialities_json = json.load(file)
with open(r'user_database.json', 'r', encoding='utf-8') as database:
    user_data = json.load(database)

##################################################################################
# создаем сущность бота
token = '2085419627:AAFaAvnPisevlhyEfpG1m8rA8kmYRlKnXG4'
bot = telebot.TeleBot(token, parse_mode=None)

####################################################### ЗАПИСИ ПЕРЕМЕННЫХ В БАЗУ ДАННЫХ ###############################################################
# форма обучения
dict_form = {
            1: 'Дневная',
            2: "Вечерняя",
            3: "Заочная",
            4: "Второе образование",
            5: "Магистратура",
            6: "Аспирантура",
            7: "Дистанционное"
        }

def get_form(message):
    try:
        form_edu = int(message.text)
        if form_edu in range(1, 8):
            user_data[message.from_user.username]['form'] = dict_form[form_edu]
        
            should_speciality(message)
    except:
        bot.send_message(message.chat.id, text='Что то тут не так...')
                
# курс
def user_faculty(message):
    try:
        if int(message.text) in range(1,7): 
            faculty = message.text
            bot.send_message(message.chat.id, 'АГа, пон')
            user_data[message.from_user.username]['course'] = ('Курс ' + faculty)
        
            should_speciality(message)
    except:
        bot.send_message(message.chat.id, text='Что то тут не так...')
        
# проверка на то, нужно ли вводить специальность или нет
def should_speciality(message):
    user_string = user_data[message.from_user.username]
    print(user_string)
    if user_string['form'] != None and user_string['course'] != None:
        ############### ЗАДАВАТЬ ПОЛЬЗОВАТЕЛЮ ВОПРОС, ПРАВИЛЬНО ЛИ ОН ВВЕЛ ВСЕ ДАННЫЕ????
        bot.send_message(message.chat.id, text='Найс!!!\nА теперь введите название вашего факультета')
        bot.register_next_step_handler(message, enter_speciality)
        
# специальность       
def user_speciality(message, dict_spec):
    try:
        speciality = dict_spec[int(message.text)]
        bot.send_message(message.chat.id, speciality)
        user_data[message.from_user.username]['speciality'] = speciality
        is_info_right(message)
    except:
        bot.send_message(message.chat.id, text='Что то тут не так...')
        
def is_info_right(message):
    for i in user_data[message.from_user.username].items():
        bot.send_message(message.chat.id, i[1])
    
    # создаем кнопки для подтверждения
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Да", )
    btn2 = types.KeyboardButton("Нет")
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, text='Всё правильно?', reply_markup=markup)
    
    bot.register_next_step_handler(message, approved)
    
######################################################################################################################

# реакция бота на /start
@bot.message_handler(commands=['start'])
def start(message):
    if message.text!= 'Нет' and message.from_user.username in user_data.keys():
        bot.send_photo(message.chat.id, 'https://sun9-28.userapi.com/impg/HBKGn-a2I3_DvKNS-U-8IigL7UUmBDmTtew5kg/j8KR3EJc7Mc.jpg?size=497x604&quality=95&sign=c68739d29dbcb863c33903b0c44f78d2&type=album')
        is_info_right(message)
    else:
        # создаем запись в таблице и записываем в колонку id ник пользователя в тг 
        user_data[message.from_user.username] = {'form': None,
                              'course': None,
                              'speciality': None}

        # создаем кнопки для ввода стартовой информации
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Ввести форму обучения")
        btn2 = types.KeyboardButton("Ввести курс")
        markup.add(btn1, btn2)

        # приветственное сообщение
        bot.send_video(message.chat.id, "https://media.tenor.com/J8XcyuI5w1QAAAAd/neco-arc-neco.gif",  reply_markup=markup)

# функция - обработчик кнопок
@bot.message_handler(content_types=['text'])
def enter_info(message):
        
    # ввод формы обучения
    if message.text == 'Ввести форму обучения':
        bot.send_message(message.chat.id, text='\n'.join([str(i) + '. ' + j for i,j in dict_form.items()]))
        bot.send_message(message.chat.id, text='Введите цифру, соответствующую Вашей форме')
        # отправляем форму обучения на запись в таблицу (мб можно через лямбда функцию записать??)
        bot.register_next_step_handler(message, get_form)
        
     # ввод курса
    elif (message.text == 'Ввести курс'):
        bot.send_message(message.chat.id, "Отправь мне цифру своего курса")
        # отправляем курс на проверку и запись
        bot.register_next_step_handler(message, user_faculty)

def enter_speciality(message):
    user_string = user_data[message.from_user.username]
    key = user_string['form'] + ',' + user_string['course']
    
    all_specialities = specialities_json[key]
    all_specialities = [i for i in all_specialities if i.lower().find(message.text.lower()) != -1]
    if len(all_specialities) == 0:
        bot.send_message(message.chat.id, text='Похоже ВЫ ввели какую то хуйню, и мы не можем ничего найти блять')
        should_speciality(message)
    else:
        dict_spec = {num:spec for num, spec in zip(range(1,len(all_specialities)+1), all_specialities)}
    
        bot.send_message(message.chat.id, 'Выбери подходящую цифру:')
        for i in dict_spec.items():
            bot.send_message(message.chat.id, str(i[0])+'. '+i[1])
        
    # отправляем факультет на запись
        bot.register_next_step_handler(message, user_speciality, dict_spec)
    
###########################################################################################################################
def approved(message):
    if message.text == 'Да':
        with open(r'user_database.json', 'w', encoding='utf-8') as file:
            json.dump(user_data, file, indent = 2, ensure_ascii=False)
        parse_raspis(message)
    elif message.text == 'Нет':
        start(message)

# МЫ ПЕРЕДЕЛАЕМ, ОТВЕЧАЮ))))))))))))))))))))))))))))))))))))))))))))))))))))))
def parse_raspis(message):
#     keyboard = types.InlineKeyboardMarkup()
#     key_continue = types.InlineKeyboardButton(text = 'СЛЕДУЮЩИЙ ДЕНЬ', callback_data = 'next')
    
    user_string = user_data[message.from_user.username]
    data = create_table(parse_rsuh(user_string['form'], user_string['course'], user_string['speciality']))
    data.to_csv('table1.csv')
    for date in data['Дата'].unique():
        
        bot.send_message(message.chat.id, '-'*30)
        bot.send_message(message.chat.id, date)
        
        data_day = data.loc[data['Дата']==date].drop('Дата', axis=1)
        data_day = data_day.transpose()
        
        for i in data_day.columns:
            bot.send_message(message.chat.id, data_day[i].to_string())
        bot.send_message(message.chat.id, 'Напишите "продолжить" для перехода на следующий день')
