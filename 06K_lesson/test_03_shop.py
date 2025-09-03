from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_shopping():
    driver = webdriver.Firefox()

    try:
        driver.get("https://www.saucedemo.com/")

        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        items = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]

        for item in items:
            driver.find_element(By.XPATH,
                                f"//div[text()='{item}']/ancestor::div[@class='inventory_item']//button").click()

        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.ID, "checkout").click()

        checkout_data = {
            "first-name": "Иван",
            "last-name": "Петров",
            "postal-code": "123456"
        }

        for field, value in checkout_data.items():
            driver.find_element(By.ID, field).send_keys(value)

        driver.find_element(By.ID, "continue").click()

        total = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "summary_total_label")))
        assert total.text == "Total: $58.29"

    finally:
        driver.quit()