from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import time

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)

try:
    driver.get("http://the-internet.herokuapp.com/inputs")
    
    time.sleep(3)

    input_field = driver.find_element(By.TAG_NAME, "input")

    input_field.send_keys("Sky")
    print("Введён текст: Sky")
    
    time.sleep(3)

    input_field.clear()
    print("Поле очищено")
    
    time.sleep(1)

    input_field.send_keys("Pro")
    print("Введён текст: Pro")
    
    time.sleep(5)

finally:
    driver.quit()
    print("Браузер Firefox закрыт")