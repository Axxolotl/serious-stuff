import telebot
from telebot import types

# импорт регулярных выражений для обработки строковых данных
import re
# импорт функций из файла, отвечающего за парсинг сайта
import RSUH_parsing_raspis
from RSUH_parsing_raspis import parse_rsuh

# импорт джейсона
import json

###################################################################мм ЧТЕНИЕ ДЖЕЙСОНОВ ##############################################################
# считываем файл со всеми специальностями и кафедрами
with open('специальности.json', 'r', encoding='utf-8') as file:
    specialities_json = json.load(file)

# считываем базу данных пользователей
with open(r'user_database.json', 'r', encoding='utf-8') as database:
    user_data = json.load(database)
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

# записываем форму обучения в джейсон
def get_form(message):
    # обработчик ошибок для проверки корректности введенных данных
    try:
        form_edu = int(message.text)
        if form_edu in range(1, 8):
            user_data[message.from_user.username]['form'] = dict_form[form_edu]
            # функция, которая проверяет, нужно ли предлагать пользователю ввести специальность, или он еще не все ввел
            should_speciality(message)
    except:
        bot.send_message(message.chat.id, text='Что то тут не так...')
                
# курс
def user_faculty(message):
    # обработчик ошибок для проверки корректности введенных данных
    try:
        if int(message.text) in range(1,7): 
            faculty = message.text
            bot.send_message(message.chat.id, 'АГа, пон')
            user_data[message.from_user.username]['course'] = ('Курс ' + faculty)
            # функция, которая проверяет, нужно ли предлагать пользователю ввести специальность, или он еще не все ввел
            should_speciality(message)
    except:
        bot.send_message(message.chat.id, text='Что то тут не так...')

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
        bot.send_message(message.chat.id, text='Что то тут не так...')
        
# проверка на то, нужно ли вводить специальность или нет
def should_speciality(message):
    # запись о пользователе из базы данных
    user_string = user_data[message.from_user.username]
    print(user_string)
    # мы предлагаем пользователю ввести специальность, если у него уже введен курс и форма обучения
    if user_string['form'] != None and user_string['course'] != None:
        bot.send_message(message.chat.id, text='Найс!!!\nА теперь введите название вашего факультета')
        bot.register_next_step_handler(message, enter_speciality)
        
####################################################### ПРОВЕРКА ДАННЫХ НА ПРАВИЛЬНОСТЬ ###################################################################мм      
def is_info_right(message):
    # отправляем пользователю всю введенную им информацию
    for i in user_data[message.from_user.username].items():
        bot.send_message(message.chat.id, i[1])
    
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
        parse_raspis(message)
    # если пользователь ввел что-то неправильно, то мы перекидываем его на старт, на начало ввода данных
    elif message.text == 'Нет':
        start(message)
#########################################################################################################################################################
################################################################### ОСНОВНАЯ ЧАСТЬ БОТА #################################################################

# реакция бота на /start
@bot.message_handler(commands=['start'])
def start(message):
    # если пользователь уже есть в базе данных, то здороваемся с ним и предлагаем проверить его данные
    if message.text != 'Нет' and message.from_user.username in user_data.keys():
        bot.send_photo(message.chat.id, 'https://sun9-28.userapi.com/impg/HBKGn-a2I3_DvKNS-U-8IigL7UUmBDmTtew5kg/j8KR3EJc7Mc.jpg?size=497x604&quality=95&sign=c68739d29dbcb863c33903b0c44f78d2&type=album')
        is_info_right(message)
    else:
        # создаем запись в базе данных и записываем в колонку id ник пользователя в тг 
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

# функция - обработчик кнопок для ввода курса и формы обучения
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
        bot.send_message(message.chat.id, text='Похоже ВЫ ввели какую то хуйню, и мы не можем ничего найти блять')
        should_speciality(message)
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

# МЫ ПЕРЕДЕЛАЕМ, ОТВЕЧАЮ))))))))))))))))))))))))))))))))))))))))))))))))))))))
def parse_raspis(message):

    user_string = user_data[message.from_user.username]
    
    raspis = parse_rsuh(user_string)
    
    ebuchiy_spisok = []
    for i in raspis[1:]:
        if len(i) == 8:
            try:
                bot.send_message(message.chat.id, ('\n'.join(ebuchiy_spisok)))
            except:
                pass
            ebuchiy_spisok = []
            bot.send_message(message.chat.id, (i[0]))
            ebuchiy_spisok.append(i[1] + ' Пара' + '\n\n' + ' | '.join(i[2:]))
        elif len(i) == 7:
            ebuchiy_spisok.append('\n' + i[0] + ' Пара' + '\n\n' + ' | '.join(i[1:]))
        else:
            ebuchiy_spisok.append(' | '.join(i))
    bot.send_message(message.chat.id, ('\n'.join(ebuchiy_spisok)))
