import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Данные
URL = "https://univer.kstu.kz/user/login"
USERNAME = os.getenv("TEST_USER")   # можно вынести в .env
PASSWORD = os.getenv("TEST_PASS")

@pytest.fixture(scope="function")
def driver():
    """Инициализация ChromeDriver"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")  # включить без графики
    service = ChromeService(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()

def test_login(driver):
    driver.get(URL)

    # Логин
    login_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
    )
    login_input.clear()
    login_input.send_keys(USERNAME)

    # Пароль
    password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    password_input.clear()
    password_input.send_keys(PASSWORD)

    # Кнопка
    login_btn = driver.find_element(By.NAME, "btn")
    login_btn.click()

    # Проверка успешного входа (например, url меняется)
    WebDriverWait(driver, 15).until(
        EC.url_contains("univer.kstu.kz/news")
    )

    assert "univer.kstu.kz" in driver.current_url