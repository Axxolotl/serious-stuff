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

driver.get(url)
time.sleep(2)
html = driver.page_source
