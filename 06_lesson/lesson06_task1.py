from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
 driver.get("http://uitestingplayground.com/ajax")

 button = WebDriverWait(driver, 10).until(
 EC.element_to_be_clickable((By.CSS_SELECTOR, "#ajaxButton.btn.btn-primary"))
 )
 button.click()

 success_message = WebDriverWait(driver, 15).until(
 EC.visibility_of_element_located((By.CSS_SELECTOR, ".bg-success"))
 )

 text = success_message.text.strip()
 print(text)

finally:
 driver.quit()