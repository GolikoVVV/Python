import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# === Страница авторизации ===
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.saucedemo.com/"

    def open(self):
        self.driver.get(self.url)
        print("✅ Открыта страница авторизации")

    def enter_username(self, username):
        username_field = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password):
        password_field = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        # Пауза 2 секунды перед нажатием Login
        print("⏳ Пауза 2 секунды перед входом...")
        time.sleep(2)

        login_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        )
        login_button.click()
        print("✅ Нажата кнопка Login")
        time.sleep(10)

# === Главная страница магазина ===
class InventoryPage:
    def __init__(self, driver):
        self.driver = driver

    def add_backpack_to_cart(self):
        add_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
        )
        add_button.click()
        print("✅ Добавлен Sauce Labs Backpack")
        time.sleep(2)

    def add_bolt_tshirt_to_cart(self):
        add_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-bolt-t-shirt"))
        )
        add_button.click()
        print("✅ Добавлен Sauce Labs Bolt T-Shirt")
        time.sleep(2)

    def add_onesie_to_cart(self):
        add_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-onesie"))
        )
        add_button.click()
        print("✅ Добавлен Sauce Labs Onesie")
        time.sleep(2)

    def go_to_cart(self):
        cart_link = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
        )
        cart_link.click()
        print("🛒 Переход в корзину")
        time.sleep(2)

# === Страница корзины ===
class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def verify_cart_has_three_items(self):
        items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(items) == 3, f"Ожидалось 3 товара, найдено: {len(items)}"
        print("✅ В корзине 3 товара")

    def click_checkout(self):
        checkout_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_button.click()
        print("✅ Нажата кнопка Checkout")


# === Страница оформления заказа ===
class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    def fill_personal_info(self, first_name, last_name, postal_code):
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "first-name"))
        ).send_keys(first_name)

        self.driver.find_element(By.ID, "last-name").send_keys(last_name)
        self.driver.find_element(By.ID, "postal-code").send_keys(postal_code)

        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()
        print("✅ Персональные данные заполнены")

    def get_total_amount(self) -> float:
        total_element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
        )
        total_text = total_element.text.strip()  # Пример: "Total: $58.29"
        return float(total_text.replace("Total: $", ""))


# === Фикстура: настройка Chrome без undetected-chromedriver ===
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    )

    # Убираем следы автоматизации
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    # Обманываем детектирование WebDriver
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false});")

    yield driver
    driver.quit()


# === Основной тест ===
def test_purchase_three_items_and_verify_total(driver):
    print("🚀 Запуск автотеста: покупка трёх товаров")

    # Создаём объекты страниц
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    # === 1. Открыть сайт ===
    login_page.open()

    # === 2. Авторизация как standard_user ===
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()  # с паузой 2 секунды

    # === 3. Добавить три товара ===
    inventory_page.add_backpack_to_cart()
    inventory_page.add_bolt_tshirt_to_cart()
    inventory_page.add_onesie_to_cart()

    # === 4. Перейти в корзину ===
    inventory_page.go_to_cart()

    # === 5. Проверить корзину и нажать Checkout ===
    cart_page.verify_cart_has_three_items()
    cart_page.click_checkout()

    # === 6. Заполнить форму ===
    checkout_page.fill_personal_info("Иван", "Иванов", "123456")

    # === 7. Получить и проверить итоговую сумму ===
    total = checkout_page.get_total_amount()
    print(f"💰 Итоговая сумма: ${total}")

    # Проверка: итоговая сумма должна быть $58.29
    assert abs(total - 58.29) < 0.01, f"Ожидалось $58.29, получено: ${total}"
    print("✅ Тест пройден: итоговая сумма верна — $58.29")