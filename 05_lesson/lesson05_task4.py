from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import time

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)

try:
    driver.get("http://the-internet.herokuapp.com/login")
    
    time.sleep(2)
    
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys("tomsmith")
    print("Логин введён: tomsmith")
    
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("SuperSecretPassword!")
    print("Пароль введён: SuperSecretPassword!")
    
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    print("Кнопка Login нажата")
    
    time.sleep(3)
    
    success_message = driver.find_element(By.CSS_SELECTOR, "#flash.success")
    message_text = success_message.text.strip()
    
    print("Текст с зелёной плашки:")
    print(message_text)

finally:
    driver.quit()
    print("Браузер закрыт")