# библиотеки для парсинга данных
import requests
from bs4 import BeautifulSoup

# библиотека для работы со временем и датами (понадобится в дальнейшем)
import datetime

# инфу будем хранить в джейсоновском формате (а зачем???)
import json

# считываем файл со специальностями (нам оттуда нужны значения кафедры)
with open('специальности.json', 'r', encoding='utf-8') as file:
    specialities_json = json.load(file)

######################################################### ПОДГОТОВКА К ПАРСИНГУ ################################################################### 
# данные будем парсить через пост запросы, а пост запросам нужны данные
# функция для получения данных в нужном формате
def create_data(user_string):
    
    # функция для проверки корректности даты (просто на сайте требуется двузначное число)
    def is_date_good(time):
        if len(time)<2:
            return '0'+time
        return time
    
    # словарь с формой обучения, потому что она по-особенному фиксируется в запросе
    form_data = {
    'Дневная': "Д",
    "Вечерняя" : "В",
    "Заочная" : "З",
    "Второе образование" : "2",
    "Магистратура" : "М",
    "Аспирантура" : "А",
    "Дистанционное" : "У"
    }
    
    # берем сегодняшнюю дату (она же начальная)
    today_date = datetime.datetime.now().date()
    # считаем конечную дату
    date_needed = today_date + datetime.timedelta(month=1)
    
    # опять создаем ключ для обращения к джейсону со специальностями
    key = user_string['form'] + ',' + user_string['course']
    
    # создаем данные для пост запроса
    data = {
        'formob' : form_data[user_string['form']],
        'kyrs' : user_string['course'].split()[1],
        'srok' : str(date_needed),
        'caf' : specialities_json[key][user_string['speciality']],
        'cafzn' : user_string['speciality'],
        'sdate_year' : str(today_date.year),
        'sdate_month': is_date_good(str(today_date.month)),
        'sdate_day' : is_date_good(str(today_date.day)),
        'fdate_year' : str(date_needed.year),
        'fdate_month': is_date_good(str(date_needed.month)),
        'fdate_day' : is_date_good(str(date_needed.day))
    }
    return data

########################################################## ПАРСЕР ДАННЫХ С САЙТА ##########################################################
def parse_rsuh(data):
    # ссылка 
    url = 'https://www.rsuh.ru/rasp/3.php'
    
    # фигашим пост запрос и парсим его
    r = requests.post(url=url, data=data)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # ищем всю инфу по расиписанию
    info = soup.findAll('tr')
    parse_data = []
    
    # запихиваем всю инфу в список для дальнейшей обработки
    for i in info:
        parse_data.append([j.text for j in i.find_all('td')])
    return parse_data
#############################################################################################################################################

# def create_table(data):
#     # создаем датафрейм с расписанием, в качестве названий колонок берем первую строку 
#     data_frame = pd.DataFrame(columns=data[0])

#     # дальше будем добавлять в датасет данные
#     for i in data[1:]:
    
#     # если длина списка равна 8, то он полный, поэтому дополнительно сохраним все эти строчки, потому что у некоторых строчек
#     # обрезана информация, наверное, чтобы не повторяться
#     # ИЛИ ПОТОМУ ЧТО РАЗРАБЫ ЕБЛАНЫ НУ КТО НАЗЫВАЕТ СУЩНОСТИ РУССКИМИ СЛОВАМИ АНГЛИЙСКИМИ БУКВАМИ БЛЯЯЯЯЯТЬ
#     # тильт
#         if len(i)==8:
#             full_info = i
#             data_frame.loc[len(data_frame.index)] = i
        
#     # если список неполный, мы добавляем к нему информацию предыдущей пары
#         else:
#             data_frame.loc[len(data_frame.index)] = list(data_frame.loc[len(data_frame.index)-1][:8-len(i)]) + i
#     return data_frame

