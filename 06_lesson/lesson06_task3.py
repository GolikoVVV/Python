from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
 driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")

 WebDriverWait(driver, 20).until(
     EC.presence_of_element_located((By.CSS_SELECTOR, "#landscape"))
 )

 images = driver.find_elements(By.TAG_NAME, "img")
 third_image_src = images[3].get_attribute("src")

 print(third_image_src)

finally:
 driver.quit()