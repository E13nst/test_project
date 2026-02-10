"""Общие фикстуры и хуки для всех сайтов"""
import allure
import pytest
from allure_commons.types import AttachmentType
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    """Настройка браузера перед каждым тестом"""
    # Инициализация ChromeDriver через webdriver-manager (для Selenium 4.x)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    # Настройка размера окна
    driver.set_window_size(1920, 1080)
    
    # Настройка selene browser (selene 2.x)
    browser.config.driver = driver
    # В selene 2.x timeout настраивается через browser.config.timeout
    browser.config.timeout = 10
    
    yield
    
    # Закрытие браузера после теста
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для прикрепления скриншотов и HTML при падении теста"""
    outcome = yield
    report = outcome.get_result()
    
    # Прикрепляем артефакты только при падении на этапе вызова теста
    if report.when == "call" and report.failed:
        try:
            # Скриншот
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="Скриншот при падении",
                attachment_type=AttachmentType.PNG,
            )
        except Exception as e:
            print(f"Не удалось прикрепить скриншот: {e}")
        
        try:
            # HTML страницы
            allure.attach(
                browser.driver.page_source,
                name="HTML страницы",
                attachment_type=AttachmentType.HTML,
            )
        except Exception as e:
            print(f"Не удалось прикрепить HTML: {e}")
        
        try:
            # URL страницы
            allure.attach(
                browser.driver.current_url,
                name="URL страницы",
                attachment_type=AttachmentType.TEXT,
            )
        except Exception as e:
            print(f"Не удалось прикрепить URL: {e}")
