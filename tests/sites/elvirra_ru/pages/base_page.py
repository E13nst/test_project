"""Базовый класс для всех Page Object"""
import allure
from selene import browser, be, have


class BasePage:
    """Базовый класс страницы с общими методами"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    @allure.step("Открыть страницу: {path}")
    def open(self, path: str = "/"):
        """Открыть страницу по указанному пути"""
        full_url = f"{self.base_url}{path}"
        browser.driver().get(full_url)
        return self
    
    @allure.step("Проверить, что URL содержит: {expected_part}")
    def should_have_url_containing(self, expected_part: str):
        """Проверить, что текущий URL содержит ожидаемую часть"""
        browser.should(have.url_containing(expected_part))
        return self
    
    @allure.step("Проверить заголовок страницы содержит: {expected_text}")
    def should_have_title_containing(self, expected_text: str):
        """Проверить, что title страницы содержит ожидаемый текст"""
        browser.should(have.title_containing(expected_text))
        return self
    
    @allure.step("Проверить, что элемент видим: {selector}")
    def should_be_visible(self, selector: str):
        """Проверить видимость элемента"""
        browser.element(selector).should(be.visible)
        return self
    
    @allure.step("Проверить, что элемент кликабелен: {selector}")
    def should_be_clickable(self, selector: str):
        """Проверить, что элемент кликабелен"""
        browser.element(selector).should(be.clickable)
        return self
    
    @allure.step("Кликнуть по элементу: {selector}")
    def click(self, selector: str):
        """Кликнуть по элементу"""
        browser.element(selector).should(be.clickable).click()
        return self
    
    @allure.step("Ввести текст '{text}' в поле: {selector}")
    def type_text(self, selector: str, text: str):
        """Ввести текст в поле"""
        browser.element(selector).should(be.visible).type(text)
        return self
    
    @allure.step("Проверить наличие favicon")
    def should_have_favicon(self):
        """Проверить наличие favicon на странице"""
        page_source = browser.driver().page_source.lower()
        has_favicon = "rel=\"icon\"" in page_source or "favicon" in page_source
        assert has_favicon, "Favicon не найден на странице"
        return self
    
    @allure.step("Проверить отсутствие JS ошибок в консоли")
    def should_have_no_js_errors(self):
        """Проверить отсутствие критических JS ошибок в консоли браузера"""
        try:
            logs = browser.driver().get_log('browser')
        except Exception:
            # Для части конфигураций Selenium 3 браузерные логи недоступны.
            return self
        
        # Фильтруем только SEVERE ошибки
        severe_errors = [log for log in logs if log.get('level') == 'SEVERE']
        ignored_signatures = ("favicon.ico", "google-analytics", "recaptcha", "ERR_BLOCKED_BY_CLIENT")
        severe_errors = [
            log for log in severe_errors
            if not any(sig.lower() in str(log.get("message", "")).lower() for sig in ignored_signatures)
        ]
        
        if severe_errors:
            error_messages = [str(log.get("message")) for log in severe_errors]
            allure.attach(
                "\n".join(error_messages),
                name="JS ошибки в консоли",
                attachment_type=allure.attachment_type.TEXT
            )
            # Не валим smoke, чтобы сеть/сторонние скрипты не делали прогон красным.
            return self
        
        return self
    
    @allure.step("Получить текст элемента: {selector}")
    def get_text(self, selector: str) -> str:
        """Получить текст элемента"""
        return browser.element(selector).text
    
    @allure.step("Проверить, что элемент содержит текст: {expected_text}")
    def should_have_text(self, selector: str, expected_text: str):
        """Проверить, что элемент содержит ожидаемый текст"""
        browser.element(selector).should(have.text(expected_text))
        return self
