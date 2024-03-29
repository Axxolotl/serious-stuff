import time
import telebot
from telebot import types

# импорт регулярных выражений для обработки строковых данных
import re
# импорт функций из файла, отвечающего за парсинг сайта
import RSUH_parsing_raspis
from RSUH_parsing_raspis import parse_rsuh


# парсинг специальностей и замена файла с ними
import parse_speciality
from parse_speciality import replace_speciality

# импорт джейсона
import json

import traceback
import sys

########################################################## LOGS #############################################################
import logging
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
###################################################################мм ЧТЕНИЕ ДЖЕЙСОНОВ ##############################################################
# считываем файл со всеми специальностями и кафедрами
with open('specialities_list.json', 'r', encoding='utf-8') as file:
    specialities_json = json.load(file)

# считываем базу данных пользователей
with open(r'user_database.json', 'r', encoding='utf-8') as database:
    user_data = json.load(database)

admins = ['saycringe', 'axxolotll']
################################################################### СОЗДАНИЕ БОТА ###################################################################

# создаем сущность бота (токен нужно будет убрать из открытого доступа)
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
# Время пар(для самых маленьких)
time = {'1':'08:45 - 10:05',
       '2':'10:15 - 11:35',
       '3':'12:10 - 13:30',
       '4':'13:40 - 15:00',
       '5':'15:35 - 16:55',
       '6':'17:05 - 18:25',
       '7':'18:50 - 20:10',
       '8':'20:20 - 21:40'}

# записываем форму обучения в джейсон
def get_form(message):
    # обработчик ошибок для проверки корректности введенных данных
    try:
        form_edu = int(message.text)
        if form_edu in range(1, 8):
            bot.send_message(message.chat.id, 'Окс, так и запишем')
            user_data[message.from_user.username]['form'] = dict_form[form_edu]
            # функция, которая проверяет, нужно ли предлагать пользователю ввести специальность, или он еще не все ввел
            should_speciality(message)
        else:
            bot.send_message(message.chat.id,'Неправильная цифра, начни заново, нажми на кнопку ещё раз!')
    except:
        bot.send_message(message.chat.id, text='Что то тут не так... лучше напиши "/start"')
                
# курс
def user_faculty(message):
    # обработчик ошибок для проверки корректности введенных данных
    try:
        if int(message.text) in range(1,7): 
            faculty = message.text
            bot.send_message(message.chat.id, 'Зафиксировали.. Честное слово, ваши данные не передаются третьим лицам:)))')
            user_data[message.from_user.username]['course'] = ('Курс ' + faculty)
            # функция, которая проверяет, нужно ли предлагать пользователю ввести специальность, или он еще не все ввел
            should_speciality(message)
        else:
            bot.send_message(message.chat.id,'Неправильная цифра, начни заново, нажми на кнопку ещё раз!')
    except:
        bot.send_message(message.chat.id, text='Что то тут не так... лучше напиши "/start"')

# специальность       
def user_speciality(message, dict_spec):
     # обработчик ошибок для проверки корректности введенных данных
    try:
        speciality = dict_spec[int(message.text)]
        bot.send_message(message.chat.id, speciality)
        user_data[message.from_user.username]['speciality'] = speciality
        
         # после введения всех данных, спрашиваем у пользователя всё ли он ввел правильно?
        is_info_right(message)
    except:
        bot.send_message(message.chat.id, text='Что то тут не так... лучше напиши "/start"')
        
# проверка на то, нужно ли вводить специальность или нет
def should_speciality(message, repeat=True):
    if message.text == '/start':
        msg = bot.reply_to(message, 'Окей, давай попробуем сначала :)')
        bot.register_next_step_handler(msg, start)
    # запись о пользователе из базы данных
    user_string = user_data[message.from_user.username]
    # мы предлагаем пользователю ввести специальность, если у него уже введен курс и форма обучения
    if user_string['form'] != None and user_string['course'] != None:
        if repeat:
            bot.send_message(message.chat.id, text='А теперь введи название своего факультета. Ты можешь не копировать свою специальность с сайта РГГУ, а ввести её аббревиатуру.\nНапример, если у тебя МПиМБ-1, можно ввести просто "мпимб" и выбрать нужную специальность из списка, отправив цифру')
        bot.register_next_step_handler(message, enter_speciality)
    else:
        bot.send_message(message.chat.id,'Для продолжения открой меню с кнопками ;)')
####################################################### ПРОВЕРКА ДАННЫХ НА ПРАВИЛЬНОСТЬ ###################################################################мм      
def is_info_right(message):
    # отправляем пользователю всю введенную им информацию
    for i in list(user_data[message.from_user.username].values())[:-1]:
        bot.send_message(message.chat.id, i)
    
    # создаем кнопки для подтверждения
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Да", )
    btn2 = types.KeyboardButton("Нет")
    markup.add(btn1, btn2)
    
    # спрашиваем у пользователя, правильно ли он ввел свои данные?
    bot.send_message(message.chat.id, text='Всё правильно?', reply_markup=markup)
    
    bot.register_next_step_handler(message, approved)

# функция, которая реагирует на ответ пользователя по нажатию кнопки
def approved(message):
    # если пользователь подтверждает правильность введенных данных, то мы 
    #1. сохраняем его в базе
    #2. парсим ему расписание
    if message.text == 'Да':
        with open(r'user_database.json', 'w', encoding='utf-8') as file:
            json.dump(user_data, file, indent = 2, ensure_ascii=False)
        parse_raspis_choose(message)
    # если пользователь ввел что-то неправильно, то мы перекидываем его на старт, на начало ввода данных
    elif message.text == 'Нет':
        start(message)
# функция определяющая на какое время парсить расписание        
def parse_raspis_choose(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("На сегодня/завтра")
    btn2 = types.KeyboardButton("На неделю")
    btn3 = types.KeyboardButton("На месяц")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'На какой срок нужно расписание?', reply_markup=markup)
    bot.register_next_step_handler(message, parse_raspis)
#########################################################################################################################################################    
################################################################### ОСНОВНАЯ ЧАСТЬ БОТА #################################################################

# реакция бота на /start
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.username
    try:
        logging.info(f"Пользователь {name} воспользовался /start {user_data[name]}")
    except:
        logging.info(f"НОВЫЙ пользователь {name} воспользовался /start {name}")
    # если пользователь уже есть в базе данных, то здороваемся с ним и предлагаем проверить его данные
    if message.text != 'Нет' and name in user_data.keys() and user_data[name]['form'] != None and user_data[name]['course'] != None and user_data[name]['speciality'] != None:
        bot.send_message(message.chat.id, 'Мы тебя помним:)')
        user_data[name]['user_id'] = message.from_user.id
        bot.send_photo(message.chat.id, 'https://sun9-28.userapi.com/impg/HBKGn-a2I3_DvKNS-U-8IigL7UUmBDmTtew5kg/j8KR3EJc7Mc.jpg?size=497x604&quality=95&sign=c68739d29dbcb863c33903b0c44f78d2&type=album')
        is_info_right(message)
    else:
        # создаем запись в базе данных и записываем в колонку id ник пользователя в тг 
        user_data[name] = {'form': None,
                              'course': None,
                              'speciality': None,
                              'user_id': message.from_user.id}

        # создаем кнопки для ввода стартовой информации
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Ввести форму обучения")
        btn2 = types.KeyboardButton("Ввести курс")
        markup.add(btn1, btn2)

        # приветственное сообщение
        bot.send_message(message.chat.id, 'Привет!')
        bot.send_video(message.chat.id, "https://media.tenor.com/J8XcyuI5w1QAAAAd/neco-arc-neco.gif",  reply_markup=markup)
        
@bot.message_handler(commands=['time'])
def get_time(message):
    time_raspis = '\n'.join([i[0]+' пара: ' + i[1] for i in time.items()])
    bot.send_message(message.chat.id, text=time_raspis)
    bot.send_message(message.chat.id, 'Что делаем дальше?')

############################################# СИСТЕМА ОПОВЕЩЕНИЙ ОТ ОДМЕНОВ ################################################    
@bot.message_handler(commands=['send'])
def send_messages(message):
    sender = message.from_user.username
    if sender in admins:
        bot.send_message(message.chat.id, 'Текст сообщения, пожалуйста')
        bot.register_next_step_handler(message, enter_and_send)
    else:
        bot.send_message(message.chat.id, f'у вас нет прав для запуска команды')
        
def enter_and_send(message):
    if message.text == '/stop':
        start(message)
    else:
        for user in user_data.keys():  
            try:
                bot.send_message(user_data[user]['user_id'],  message.text)
                time.sleep(1)
            except Exception as e:
                bot.send_message(message.chat.id, f'ошибка отправки сообщения юзеру - {user}')

##################################################### ЗАМЕНА СПЕЦИАЛЬНОСТЕЙ НА НОВЫЕ КАЙФ ######################################################
@bot.message_handler(commands=['replacesp'])
def replace_sp(message):
    sender = message.from_user.username
    if sender in admins:
        bot.send_message(message.chat.id, 'Парсим, подождите')
        replace_speciality()
        bot.send_message(message.chat.id, 'Готово... Вроде')
    else:
        bot.send_message(message.chat.id, f'у вас нет прав для запуска команды')
###################################################################################################################################           
# функция - обработчик кнопок для ввода курса и формы обучения
@bot.message_handler(content_types=['text'])
def enter_info(message):
        
    # ввод формы обучения
    if message.text == 'Ввести форму обучения':
        bot.send_message(message.chat.id, text='\n'.join([str(i) + '. ' + j for i,j in dict_form.items()]))
        bot.send_message(message.chat.id, text='Введи цифру, соответствующую твоей форме')
        # отправляем форму обучения на запись в таблицу (мб можно через лямбда функцию записать??)
        bot.register_next_step_handler(message, get_form)
        
     # ввод курса
    elif (message.text == 'Ввести курс'):
        bot.send_message(message.chat.id, "Отправь мне цифру своего курса")
        # отправляем курс на проверку и запись
        bot.register_next_step_handler(message, user_faculty)

# функция для ввода специальности пользователя (срабатывает после введения курса и формы обучения) 
def enter_speciality(message):
    # сохраняем строку с информацией пользователя
    user_string = user_data[message.from_user.username]
    
    # специальности в джейсоне записаны как словари с ключами в виде формы обучения + курс, поэтому создаем строку для обращения к ним
    key = user_string['form'] + ',' + user_string['course']
    
    # берем все специальности по ключу
    all_specialities = specialities_json[key]
    # ищем среди них подходящие под то, что ввел пользователь
    all_specialities = [i for i in all_specialities if i.lower().find(message.text.lower()) != -1]
    
    # проверка на наличие подходящих факультетов
    if len(all_specialities) == 0:
        # немного пассивной агрессииЮ потому что СЛОЖНАААААААААААА
        if message.text == '/start':
            start(message)
        else:
            bot.send_message(message.chat.id, text='Я не смог найти твою специальность, попробуй ещё раз!\nЕсли ты думаешь, что неправильно указал(а) форму обучения или курс - напиши /start!')
            should_speciality(message, False)
    else:
        # если все норм, то создаем словарь с перечнем подходящих специальностей с индексами
        dict_spec = {num:spec for num, spec in zip(range(1,len(all_specialities)+1), all_specialities)}
        
        # отправляем инфу пользователю
        bot.send_message(message.chat.id, 'Выбери подходящую цифру:')
        for i in dict_spec.items():
            bot.send_message(message.chat.id, str(i[0])+'. '+i[1])
        
    # отправляем факультет на запись
        bot.register_next_step_handler(message, user_speciality, dict_spec)
    
###########################################################################################################################


# МЫ ПЕРЕДЕЛАЕМ, ОТВЕЧАЮ))))))))))))))))))))))))))))))))))))))))))))))))))))))(переделали)
def parse_raspis(message):
    
    user_string = user_data[message.from_user.username]
    
    raspis = parse_rsuh(user_string, message)
    
    lessons_list = []
    for i in raspis[1:]:
        i[-3] = '<i>'+i[-3]+'</i>'
        if len(i) == 8:
            try:
                bot.send_message(message.chat.id, ('\n'.join(lessons_list)), parse_mode="HTML")
            except:
                pass
            lessons_list = []
            bot.send_message(message.chat.id, (i[0]))
            lessons_list.append(i[1] + ' Пара' + '     ' + time[i[1]] + '\n\n' + ' | '.join(i[2:]))
        elif len(i) == 7:
            lessons_list.append('\n' + i[0] + ' Пара'+ '     ' + time [i[0]] + '\n\n' + ' | '.join(i[1:]))
        else:
            lessons_list.append(' | '.join(i))
    if not lessons_list:
        bot.send_message(message.chat.id, 'Похоже, что на выбранную дату у тебя нет занятий, можешь отдыхать ;)')
    else:
        bot.send_message(message.chat.id, ('\n'.join(lessons_list)), parse_mode="HTML")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/start")
    btn2 = types.KeyboardButton("/time")
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, '( ͡° ͜ʖ ͡°)', reply_markup=markup)

bot.infinity_polling()
