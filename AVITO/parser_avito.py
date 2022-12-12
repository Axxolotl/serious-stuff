from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import time
import json

# создание драйвера селениума
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

############################################################## ФУНКЦИЯ ПОЛУЧЕНИЯ НОМЕРА ПОСЛЕДНЕЙ СТРАНИЦЫ ##############################################
url = 'https://www.avito.ru/all/noutbuki?cd=1&p=1&q=macbook'

def get_last(url):
    driver.get(url)
    time.sleep(2)
    
    html = driver.page_source
    
    soup = BeautifulSoup(html, 'lxml')
    last = int(soup.find_all(class_='pagination-item-JJq_j')[-2].text)
    
    return last
#########################################################################################################################################################  
avito = 'www.avito.ru'

n = get_last(url)
names = []
links = []
prices = []

for i in range(1, n): 
    url = f'https://www.avito.ru/all/noutbuki?cd=1&p={i}&q=macbook'
    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    
    soup = BeautifulSoup(html, 'lxml')
    names_temp = soup.find_all(class_='title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO')
    names += [i.text for i in names_temp]
    
    refs = soup.find_all(class_='iva-item-titleStep-pdebR')
    links += [avito + i.find('a').get('href') for i in refs]

    prices_temp = soup.find_all(attrs={'itemprop':'price'})
    prices += [i.get('content') for i in prices_temp]
