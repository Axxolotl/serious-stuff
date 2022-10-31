import re

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
    form_edu = int(message.text)
    if form_edu in range(1, 8):
        user_data[message.from_user.username]['form'] = dict_form[form_edu]
        
        should_speciality(message)
    else:
        bot.send_message(message.chat.id, text='Пошел нахуй')
                
# курс
def user_faculty(message):
    if int(message.text) in range(1,7): 
        faculty = message.text
        bot.send_message(message.chat.id, 'АГа, пон')
        user_data[message.from_user.username]['course'] = ('Курс ' + faculty)
        
        should_speciality(message)

        
# проверка на то, нужно ли вводить специальность или нет
def should_speciality(message):
    user_string = user_data[message.from_user.username]
    print(user_string)
    if user_string['form'] != None and user_string['course'] != None:
        ############### ЗАДАВАТЬ ПОЛЬЗОВАТЕЛЮ ВОПРОС, ПРАВИЛЬНО ЛИ ОН ВВЕЛ ВСЕ ДАННЫЕ????
        bot.send_message(message.chat.id, text='Найс!!!\nА теперь введите название вашего факультета')
        bot.register_next_step_handler(message, enter_speciality)
        
# специальность       
def user_speciality(message):
    speciality = globals()['dict_spec'][int(message.text)]
    bot.send_message(message.chat.id, speciality)
    user_data[message.from_user.username]['speciality'] = speciality
    
    for i in user_data[message.from_user.username].items():
        bot.send_message(message.chat.id, i[0]+': '+i[1])
    
    # создаем кнопки для подтверждения
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Да")
    btn2 = types.KeyboardButton("Нет")
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, text='Всё правильно?', reply_markup=markup)
    
    bot.register_next_step_handler(message, approved)
    
######################################################################################################################

# реакция бота на /start
@bot.message_handler(commands=['start'])
def start(message):
    # создаем запись в таблице и записываем в колонку id ник пользователя в тг (нужно потом сделать проверку на существование пользователя в базе)
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
    
    dict_spec = {num:spec for num, spec in zip(range(1,len(all_specialities)+1), all_specialities)}
    globals()['dict_spec'] = dict_spec
    
    bot.send_message(message.chat.id, 'Выбери подходящую цифру:')
    for i in dict_spec.items():
        bot.send_message(message.chat.id, str(i[0])+'. '+i[1])
        
    # отправляем факультет на запись
    bot.register_next_step_handler(message, user_speciality)
    
###########################################################################################################################
def approved(message):
    if message.text == 'Да':
        with open(r'C:\Users\azaza\OneDrive\Desktop\работа\user_database.json', 'w', encoding='utf-8') as file:
            json.dump(user_data, file, indent = 2, ensure_ascii=False)
