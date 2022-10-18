import requests
from bs4 import BeautifulSoup

import pandas as pd

url = 'https://www.mayak-agent.ru/actresses'
req = requests.get(url)

soup = BeautifulSoup(req.text, 'lxml')

actresses = soup.find(class_ = 'row bottom20px').find_all('a')
hrefs = ['https://www.mayak-agent.ru' + i.get('href') for i in actresses]
