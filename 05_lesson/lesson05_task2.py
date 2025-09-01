from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome()

try:
    driver.get("http://uitestingplayground.com/dynamicid")
    time.sleep(3)
    button = driver.find_element(By.CSS_SELECTOR, ".btn-primary")
    button.click()

    time.sleep(5)

    print("Клик по синей кнопке c Dynamic ID состоялся.")

finally:
    driver.quit()