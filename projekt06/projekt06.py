import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

save_path = r'C:\Users\wsszo\PycharmProjects\pwzn\projekt06\cheese_info.json'
url = 'https://krainaserow.pl/catalog?filter_all_categories=15'

options = Options()
service = Service(r'C:\Users\wsszo\PycharmProjects\pwzn\projekt06\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)
button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nety_close_button')))
button.click()

podglad_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                'body > div.container.justify-content-center > div.row > div.col-12.col-lg-9 > div > div:nth-child(2) > div > div > div > div > button')))
podglad_button.click()

time.sleep(5)

data = driver.find_element(By.CSS_SELECTOR,
                           '#modal_40 > div > div > div.card.modal-body.border-0.mb-0.d-flex.d-xl-none > div > div > div > div:nth-child(3) > div > p')
info = data.text.strip()

with open(save_path, 'w') as file:
    json.dump(info, file)

zamknij_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                '#modal_40 > div > div > div.card.modal-body.border-0.mb-0.d-flex.d-xl-none > div > div > div > div.col-12.col-md-12.mt-2 > button')))
zamknij_button.click()

for _ in range(100):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)

time.sleep(5)
driver.close()
