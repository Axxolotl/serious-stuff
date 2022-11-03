from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import requests
import time
import json

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# url сайта рггу
url = 'https://www.rsuh.ru/raspis/'
driver.get(url)
time.sleep(2)

req = requests.get(url)
soup = BeautifulSoup(req.text, 'lxml')

form = [i.text.strip() for i in soup.find(attrs = {'id': 'formob'})]
form.sort()
del form[0:8]
course = [i.text.strip() for i in soup.find(attrs = {'id':'kyrs'})]
course.sort()
del course[0:7]
specialities = {}

for edu_form in form:
    for course_num in course:
    # в общем тут мы просто выставляем значения у выпадающих списков
        for i in zip(['formob', 'kyrs'], [edu_form, course_num]):
            select = Select(driver.find_element(By.ID, i[0]))
            select.select_by_visible_text(i[1])
        # жмякаем на кнопку "продолжить"
        continue_ = driver.find_element(By.ID, 'filters').click()
        time.sleep(2)
        soup = BeautifulSoup(driver.find_element(By.ID, 'caf').get_attribute('innerHTML'), 'lxml')
        groups = [i.text.strip() for i in soup.find_all('option')]
        caf = [i.get('value') for i in soup.find_all('option')]
        specialities[str(edu_form + ',' + course_num)] = {i:j for i,j in zip(groups, caf)}
        
with open (r'специальности.json', 'w', encoding='utf-8') as file:
    json.dump(specialities, file, indent = 2, ensure_ascii=False)
