import requests
from bs4 import BeautifulSoup

import pandas as pd

url = 'https://www.mayak-agent.ru/actresses'
req = requests.get(url)

soup = BeautifulSoup(req.text, 'lxml')

actresses = soup.find(class_ = 'row bottom20px').find_all('a')
hrefs = ['https://www.mayak-agent.ru' + i.get('href') for i in actresses]


class_names = ['personal-wrapper', 'details-wrapper']
nums_names = ['6', '12']
personal_info = ''
for i,j in zip(class_names, nums_names):
    
    personal = w_soup.find(class_ = i).find(class_ = 'row').find_all(class_ = f'col-xs-{j} col-md-8')
    personal = [re.sub(r'[\n|\r|\t]', ' ', i.text).strip() for i in personal]

    labels = w_soup.find(class_ = i).find(class_ = 'row').find_all(class_ = f'col-xs-{j} col-md-4 labels')
    labels = [re.sub(r'[\n|\r|\t]', '', i.text).strip() for i in labels]
    
    if i == 'personal-wrapper':
        personal_info += '<br />'.join([i + ' ' + j for i,j in zip(labels, personal)]) + '<br />___________________________________________________________________<br />'
    else:
        personal_info += '<br /><br />'.join([i + ' ' + j for i,j in zip(labels, personal)]).replace('     ', '<br /><br />')
        
ssl = a_soup.find(class_='details-wrapper').find(class_='col-xs-12 links').find(class_='row').find(class_='col-xs-12 col-md-8').find_all('a')
