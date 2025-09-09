import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from typing import Generator


# === Страница авторизации ===
@allure.epic("Web UI Тесты")
@allure.feature("Авторизация и покупка")
class LoginPage:
    """
    Класс для взаимодействия со страницей авторизации.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы авторизации.

        :param driver: Экземпляр веб-драйвера Chrome.
        """
        self.driver = driver
        self.url: str = "https://www.saucedemo.com/"

    @allure.step("Открытие страницы авторизации")
    def open(self) -> None:
        """
        Открывает страницу авторизации.
        """
        self.driver.get(self.url)
        print("✅ Открыта страница авторизации")

    @allure.step("Ввод логина: {username}")
    def enter_username(self, username: str) -> None:
        """
        Вводит имя пользователя в поле ввода.

        :param username: Логин пользователя (строка).
        """
        username_field = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        username_field.clear()
        username_field.send_keys(username)

    @allure.step("Ввод пароля")
    def enter_password(self, password: str) -> None:
        """
        Вводит пароль в поле ввода.

        :param password: Пароль пользователя (строка).
        """
        password_field = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.clear()
        password_field.send_keys(password)

    @allure.step("Нажатие кнопки Login")
    def click_login(self) -> None:
        """
        Нажимает кнопку входа с паузой 2 секунды перед нажатием.
        """
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
    """
    Класс для взаимодействия с главной страницей товаров.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы товаров.

        :param driver: Экземпляр веб-драйвера Chrome.
        """
        self.driver = driver

    @allure.step("Добавление Sauce Labs Backpack в корзину")
    def add_backpack_to_cart(self) -> None:
        """
        Добавляет рюкзак в корзину.
        """
        add_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
        )
        add_button.click()
        print("✅ Добавлен Sauce Labs Backpack")
        time.sleep(2)

    @allure.step("Добавление Sauce Labs Bolt T-Shirt в корзину")
    def add_bolt_tshirt_to_cart(self) -> None:
        """
        Добавляет футболку в корзину.
        """
        add_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-bolt-t-shirt"))
        )
        add_button.click()
        print("✅ Добавлен Sauce Labs Bolt T-Shirt")
        time.sleep(2)

    @allure.step("Добавление Sauce Labs Onesie в корзину")
    def add_onesie_to_cart(self) -> None:
        """
        Добавляет комбинезон в корзину.
        """
        add_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-onesie"))
        )
        add_button.click()
        print("✅ Добавлен Sauce Labs Onesie")
        time.sleep(2)

    @allure.step("Переход в корзину")
    def go_to_cart(self) -> None:
        """
        Переходит в корзину по клику на иконку.
        """
        cart_link = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
        )
        cart_link.click()
        print("🛒 Переход в корзину")
        time.sleep(2)


# === Страница корзины ===
class CartPage:
    """
    Класс для взаимодействия с корзиной.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы корзины.

        :param driver: Экземпляр веб-драйвера Chrome.
        """
        self.driver = driver

    @allure.step("Проверка: в корзине 3 товара")
    def verify_cart_has_three_items(self) -> None:
        """
        Проверяет, что в корзине ровно 3 товара.
        """
        items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        with allure.step(f"Проверка количества товаров: ожидается 3, найдено {len(items)}"):
            assert len(items) == 3, f"Ожидалось 3 товара, найдено: {len(items)}"
        print("✅ В корзине 3 товара")

    @allure.step("Нажатие кнопки Checkout")
    def click_checkout(self) -> None:
        """
        Нажимает кнопку оформления заказа.
        """
        checkout_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_button.click()
        print("✅ Нажата кнопка Checkout")


# === Страница оформления заказа ===
class CheckoutPage:
    """
    Класс для взаимодействия со страницей оформления заказа.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы оформления.

        :param driver: Экземпляр веб-драйвера Chrome.
        """
        self.driver = driver

    @allure.step("Заполнение персональных данных")
    def fill_personal_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """
        Заполняет форму персональных данных.

        :param first_name: Имя.
        :param last_name: Фамилия.
        :param postal_code: Почтовый индекс.
        """
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "first-name"))
        ).send_keys(first_name)

        self.driver.find_element(By.ID, "last-name").send_keys(last_name)
        self.driver.find_element(By.ID, "postal-code").send_keys(postal_code)

        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()
        print("✅ Персональные данные заполнены")

    @allure.step("Получение итоговой суммы")
    def get_total_amount(self) -> float:
        """
        Получает итоговую сумму со страницы.

        :return: Итоговая сумма как число (float).
        """
        total_element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
        )
        total_text = total_element.text.strip()  # Пример: "Total: $58.29"
        return float(total_text.replace("Total: $", ""))


# === Фикстура: настройка Chrome ===
@pytest.fixture
def driver() -> Generator[WebDriver, None, None]:
    """
    Фикстура: создаёт и настраивает экземпляр Chrome-драйвера.

    :yield: Настроенный экземпляр WebDriver.
    """
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

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false});")

    yield driver
    driver.quit()


# === Основной тест ===
@allure.title("Покупка трёх товаров и проверка итоговой суммы")
@allure.description("""
Тест проверяет:
1. Авторизацию пользователя.
2. Добавление трёх товаров в корзину.
3. Переход в корзину и оформление заказа.
4. Проверку итоговой суммы на странице подтверждения.
""")
@allure.feature("Оформление заказа")
@allure.severity(allure.severity_level.CRITICAL)
def test_purchase_three_items_and_verify_total(driver: WebDriver) -> None:
    """
    Основной тест: покупка трёх товаров и проверка итоговой суммы.

    :param driver: Экземпляр веб-драйвера Chrome.
    """
    print("🚀 Запуск автотеста: покупка трёх товаров")

    # Создаём объекты страниц
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    # === 1. Открыть сайт ===
    login_page.open()

    # === 2. Авторизация ===
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()

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

    with allure.step(f"Проверка итоговой суммы: ожидается $58.29, получено ${total}"):
        assert abs(total - 58.29) < 0.01, f"Ожидалось $58.29, получено: ${total}"
    print("✅ Тест пройден: итоговая сумма верна — $58.29")