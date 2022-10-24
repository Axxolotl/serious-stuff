
# библиотеки для работы с селениумом
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

# time для задержек при работе с селениумом
import time

# суп для удобного парсинга
from bs4 import BeautifulSoup
import requests

# конечный словарь будем записывать в json
import json

# url сайта рггу
url = 'https://www.rsuh.ru/raspis/'

# словарь для хранения специальностей по форме обучения и курсу
specialities = {}

############################################## парсим все формы обучения и группы ###########################################
req = requests.get(url)
soup = BeautifulSoup(req.text, 'lxml')

form = [i.text.strip() for i in soup.find(attrs = {'id': 'formob'})]
form.sort()
del form[0:8]
course = [i.text.strip() for i in soup.find(attrs = {'id':'kyrs'})]
course.sort()
del course[0:7]

######################################################### SELENIUM #############################################################
# опции для того, чтобы селениум работал с браузером в фоновом режиме
chrome_options = Options()
chrome_options.add_argument("--headless")

# создаем драйвер для селениума
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.get(url)
time.sleep(2)

# цикл, который собирает все специальности в словарь по ключу (форма обучения, курс)
for edu_form in form:
    for course_num in course:
    # в общем тут мы просто выставляем значения у выпадающих списков
        for i in zip(['formob', 'kyrs'], [edu_form, course_num]):
            select = Select(driver.find_element(By.ID, i[0]))
            select.select_by_visible_text(i[1])
        # жмякаем на кнопку "продолжить"
        continue_ = driver.find_element(By.ID, 'filters').click()
        time.sleep(2)
        
        # ищем специальности с помощью супа
        soup = BeautifulSoup(driver.find_element(By.ID, 'caf').get_attribute('innerHTML'), 'lxml')
        groups = [i.text.strip() for i in soup.find_all('option')]
        specialities[edu_form, course_num] = groups
