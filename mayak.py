import hashlib
import requests
from bs4 import BeautifulSoup

import re
import pandas as pd

from get_infofunc import get_personal_info

cal = ['Tilda UID', 'Brand', 'SKU', 'Mark', 'Category', 'Title', 'Description', 'Text', 'Photo', 'Price',
       'Quantity','Price Old','Editions','Modifications','External ID','Parent UID','Weight',
       'Length','Width','Height','Url']

dataframe = pd.DataFrame(columns=cal)
url = 'https://www.mayak-agent.ru/actresses'
req = requests.get(url)

soup = BeautifulSoup(req.text, 'lxml')

actresses = soup.find(class_ = 'row bottom20px').find_all('a')
hrefs = ['https://www.mayak-agent.ru' + i.get('href') for i in actresses]
actors = soup.find(class_='row bottom20px').find_all('a')
actors_hrefs = ['https://www.mayak-agent.ru' + i.get('href') for i in actors]
hrefs.extend(actors_hrefs)

for link in hrefs:
    woman = requests.get(link)
    w_soup = BeautifulSoup(woman.text, 'lxml')
    
    photos = [i.find('img')['src'] for i in w_soup.find_all(class_='swiper-slide')]
    name = w_soup.find('h1').text.strip()
    pers_info = get_personal_info(w_soup)
    uuid = int(hashlib.sha256(name.encode('utf-8')).hexdigest(), 16) % 10**12

    dataframe.loc[len(dataframe.index)-1] = [uuid, '', '', '', '', name.upper(), '', pers_info, ' '.join(photos), '', '', '', '', '', '','','','','','','']

dataframe.to_csv('store.csv')



url = 'https://www.mayak-agent.ru/'
gender = ['actresses', 'actors']
hrefs = []

for i in gender:
    req = requests.get(url+i)

    soup = BeautifulSoup(req.text, 'lxml')

    act = soup.find(class_ = 'row bottom20px').find_all('a')
    hrefs += ['https://www.mayak-agent.ru' + i.get('href') for i in act]
