from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import time
import json

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

url = 'https://www.avito.ru/all/noutbuki?cd=1&p=1&q=macbook'
url1 = 'www.avito.ru'

driver.get(url)
time.sleep(2)
html = driver.page_source

soup = BeautifulSoup(html, 'lxml')
models = soup.find_all(class_='title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO')
models = [i.text for i in headers]

refs = soup.find_all(class_='iva-item-titleStep-pdebR')
links = [url1 + i.find('a').get('href') for i in refs]

prices = soup.find_all(attrs={'itemprop':'price'})
prices = [i.get('content') for i in prices]
