from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

try:
    driver.get("http://uitestingplayground.com/classattr")
    time.sleep(3)
    button = driver.find_element(By.CSS_SELECTOR, ".btn-primary")
    button.click()

    time.sleep(5)

    print("Клик по синей кнопке состоялся.")

finally:
    driver.quit()