#!/usr/bin/env python
# coding: utf-8

# In[62]:


# я хочу загрузить полученные данные в pandas.DataFrame. В таблицу то есть.
import pandas as pd

import datetime

import requests

from bs4 import BeautifulSoup
import json


# In[63]:


with open('специальности.json', 'r', encoding='utf-8') as file:
    specialities_json = json.load(file)


# In[75]:


def create_data(user_string):
    
    def is_date_good(time, month=False):
        if month and int(time)>12:
            time = '1'
        if len(time)<2:
            return '0'+time
        return time
    
    form_data = {
    'Дневная': "Д",
    "Вечерняя" : "В",
    "Заочная" : "З",
    "Второе образование" : "2",
    "Магистратура" : "М",
    "Аспирантура" : "А",
    "Дистанционное" : "У"
    }
    
    today_date = datetime.datetime.now().date()
    
    date_needed = today_date + datetime.timedelta(days=7)
    key = user_string['form'] + ',' + user_string['course']
    
    data = {
        'formob' : form_data[user_string['form']],
        'kyrs' : user_string['course'].split()[1],
        'srok' : str(date_needed),
        'caf' : specialities_json[key][user_string['speciality']],
        'cafzn' : user_string['speciality'],
        'sdate_year' : str(today_date.year),
        'sdate_month': is_date_good(str(today_date.month),month=True),
        'sdate_day' : is_date_good(str(today_date.day)),
        'fdate_year' : str(date_needed.year),
        'fdate_month': is_date_good(str(int(today_date.month)+1), month=True),
        'fdate_day' : is_date_good(str(today_date.day))
    }
    return data


# In[76]:


create_data({"form": "Дневная",
    "course": "Курс 4",
    "speciality": "ОИС_ИС (Группа: 1)"})


# In[88]:


def parse_rsuh(data):
    url = 'https://www.rsuh.ru/rasp/3.php'
    
    r = requests.post(url=url, data=data)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    info = soup.findAll('tr')
    parse_data = []
    
    for i in info:
        parse_data.append([j.text for j in i.find_all('td')])
    return parse_data


# In[89]:


parse_rsuh(create_data({"form": "Дневная",
    "course": "Курс 4",
    "speciality": "ОИС_ИС (Группа: 1)"}))


# In[34]:


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

