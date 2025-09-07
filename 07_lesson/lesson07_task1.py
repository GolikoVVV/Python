import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# === Класс страницы калькулятора ===
class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
        self.delay_input = "#delay"
        self.screen = ".screen"
        self.buttons = {
            "7": "//span[text()='7']",
            "8": "//span[text()='8']",
            "+": "//span[text()='+']",
            "=": "//span[text()='=']"
        }

    def open(self):
        """Открыть страницу калькулятора."""
        self.driver.get(self.url)

    def set_delay(self, seconds: str):
        """Ввести значение задержки."""
        delay_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.delay_input))
        )
        delay_field.clear()
        delay_field.send_keys(seconds)

    def click_button(self, key: str):
        """Нажать кнопку по имени."""
        button = self.driver.find_element(By.XPATH, self.buttons[key])
        button.click()

    def get_result(self) -> str:
        """Получить текст результата с экрана."""
        result_element = WebDriverWait(self.driver, 50).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, self.screen), "15"),
            message="Результат не стал '15' за отведённое время"
        )
        return self.driver.find_element(By.CSS_SELECTOR, self.screen).text.strip()


# === Фикстура для драйвера ===
@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()


# === Тест ===
def test_slow_calculator_single_file(driver):
    # Создаём объект страницы
    calc_page = CalculatorPage(driver)

    # Выполняем действия (никаких find_element в тесте!)
    calc_page.open()
    calc_page.set_delay("46")
    calc_page.click_button("7")
    calc_page.click_button("+")
    calc_page.click_button("8")
    calc_page.click_button("=")

    # Проверка результата
    result = calc_page.get_result()
    assert result == "15", f"Ожидался результат '15', но получено: '{result}'"

    print(f"✅ Результат верный: {result}")