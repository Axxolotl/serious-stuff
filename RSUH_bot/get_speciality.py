# судя по всему, для парсинга расписания нам понадобиться доставать инфу через selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

import time

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# url сайта рггу
url = 'https://www.rsuh.ru/raspis/'
driver.get(url)
time.sleep(2)

form =  ["Дневная", "Вечерняя","Заочная","Второе образование", "Магистратура","Аспирантура", "Дистанционное"]
course = ['Курс ' + str(i) for i in range(1,7)]


for edu_form in form:
    for course_num in course:
    # в общем тут мы просто выставляем значения у выпадающих списков
        for i in zip(['formob', 'kyrs'], [edu_form, course_num]):
            select = Select(driver.find_element(By.ID, i[0]))
            select.select_by_visible_text(i[1])
    
        # жмякаем на кнопку "продолжить"
        continue_ = driver.find_element(By.ID, 'filters').click()
        time.sleep(2)
