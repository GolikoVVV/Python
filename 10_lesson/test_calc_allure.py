import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# === Класс страницы калькулятора ===
@allure.epic("Web UI Тесты")
@allure.feature("Калькулятор")
class CalculatorPage:
    """
    Класс для взаимодействия со страницей медленного калькулятора.
    Реализует паттерн Page Object.
    """

    def __init__(self, driver: webdriver.Chrome) -> None:
        """
        Инициализация страницы.

        :param driver: Экземпляр веб-драйвера Chrome.
        """
        self.driver = driver
        self.url: str = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
        self.delay_input: str = "#delay"
        self.screen: str = ".screen"
        self.buttons: dict[str, str] = {
            "7": "//span[text()='7']",
            "8": "//span[text()='8']",
            "+": "//span[text()='+']",
            "=": "//span[text()='=']"
        }

    @allure.step("Открытие страницы калькулятора")
    def open(self) -> None:
        """
        Открывает страницу калькулятора.
        """
        self.driver.get(self.url)

    @allure.step("Установка задержки: {seconds} секунд")
    def set_delay(self, seconds: str) -> None:
        """
        Вводит значение задержки в поле ввода.

        :param seconds: Значение задержки в виде строки (например, "45").
        """
        delay_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.delay_input))
        )
        delay_field.clear()
        delay_field.send_keys(seconds)

    @allure.step("Нажатие кнопки: {key}")
    def click_button(self, key: str) -> None:
        """
        Нажимает кнопку калькулятора по имени.

        :param key: Ключ кнопки (например, '7', '+', '=').
        """
        button = self.driver.find_element(By.XPATH, self.buttons[key])
        button.click()

    @allure.step("Ожидание результата '15' на экране")
    def get_result(self) -> str:
        """
        Ожидает появления результата '15' на экране и возвращает его.

        :return: Текст результата с экрана (например, '15').
        """
        WebDriverWait(self.driver, 50).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, self.screen), "15"),
            message="Результат не стал '15' за отведённое время"
        )
        return self.driver.find_element(By.CSS_SELECTOR, self.screen).text.strip()


# === Фикстура для драйвера ===
@pytest.fixture
def driver():
    """
    Фикстура: создаёт и закрывает экземпляр Chrome-драйвера.
    """
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()


# === Тест ===
@allure.title("Сложение 7 + 8 с задержкой")
@allure.description("Проверка, что калькулятор корректно складывает 7 и 8 с задержкой 46 секунд.")
@allure.feature("Сложение")
@allure.severity(allure.severity_level.CRITICAL)
def test_slow_calculator_single_file(driver):
    """
    Тест: складывает 7 и 8 на медленном калькуляторе с задержкой.
    Проверяет, что результат равен 15.
    """
    # Создаём объект страницы
    calc_page = CalculatorPage(driver)

    # Действия
    calc_page.open()
    calc_page.set_delay("46")
    calc_page.click_button("7")
    calc_page.click_button("+")
    calc_page.click_button("8")
    calc_page.click_button("=")

    # Проверка результата
    result = calc_page.get_result()
    with allure.step(f"Проверка: результат равен '15'. Получено: '{result}'"):
        assert result == "15", f"Ожидался результат '15', но получено: '{result}'"

    print(f"✅ Результат верный: {result}")