"""Компонент формы (переиспользуемый)"""
import allure
from selene import browser, be, have


class FormComponent:
    """Компонент формы для проверки полей и валидаций"""
    
    @allure.step("Проверить, что поле '{field_selector}' видимо")
    def should_have_field(self, field_selector: str):
        """Проверить наличие поля"""
        browser.element(field_selector).should(be.visible)
        return self
    
    @allure.step("Проверить, что обязательное поле помечено '*'")
    def should_have_required_marker(self, field_selector: str):
        """Проверить, что у обязательного поля есть маркер '*'"""
        # Проверяем атрибут required или наличие * в label
        field = browser.element(field_selector)
        
        # Проверяем либо атрибут required
        has_required_attr = field.locate().get_attribute("required") is not None
        
        # Либо ищем * в связанном label
        has_asterisk = False
        try:
            field_id = field.locate().get_attribute("id")
            if field_id:
                label = browser.element(f'label[for="{field_id}"]')
                if "*" in label.locate().text:
                    has_asterisk = True
        except:
            pass
        
        # Или просто проверяем родительский элемент на наличие *
        try:
            parent_text = field.locate().find_element_by_xpath("..").text
            if "*" in parent_text:
                has_asterisk = True
        except:
            pass
        
        assert has_required_attr or has_asterisk, f"Обязательное поле {field_selector} не помечено '*'"
        return self
    
    @allure.step("Проверить наличие placeholder у поля '{field_selector}'")
    def should_have_placeholder(self, field_selector: str):
        """Проверить, что у поля есть placeholder"""
        field = browser.element(field_selector)
        placeholder = field.locate().get_attribute("placeholder")
        
        assert placeholder and len(placeholder) > 0, f"У поля {field_selector} отсутствует placeholder"
        allure.attach(
            placeholder,
            name=f"Placeholder поля {field_selector}",
            attachment_type=allure.attachment_type.TEXT
        )
        return self
    
    @allure.step("Ввести текст '{text}' в поле '{field_selector}'")
    def fill_field(self, field_selector: str, text: str):
        """Заполнить поле текстом"""
        browser.element(field_selector).should(be.visible).type(text)
        return self
    
    @allure.step("Очистить поле '{field_selector}'")
    def clear_field(self, field_selector: str):
        """Очистить поле"""
        browser.element(field_selector).clear()
        return self
    
    @allure.step("Проверить сообщение об ошибке валидации")
    def should_have_validation_error(self, error_selector: str = ".error, .invalid-feedback, [class*='error']"):
        """Проверить наличие сообщения об ошибке валидации"""
        browser.element(error_selector).should(be.visible)
        return self
    
    @allure.step("Проверить сообщение об успешной отправке формы")
    def should_have_success_message(self, success_selector: str = ".success, .alert-success, [class*='success']"):
        """Проверить наличие сообщения об успехе"""
        browser.element(success_selector).should(be.visible)
        return self
    
    @allure.step("Отправить форму")
    def submit(self, submit_button_selector: str = "button[type='submit'], input[type='submit']"):
        """Отправить форму"""
        browser.element(submit_button_selector).should(be.clickable).click()
        return self
    
    @allure.step("Проверить, что поле доступно с клавиатуры (focusable)")
    def should_be_keyboard_accessible(self, field_selector: str):
        """Проверить, что поле можно сфокусировать с клавиатуры"""
        field = browser.element(field_selector).locate()
        
        # Проверяем, что элемент может получить фокус
        # (не имеет tabindex="-1" и не disabled)
        tabindex = field.get_attribute("tabindex")
        is_disabled = field.get_attribute("disabled")
        
        assert tabindex != "-1", f"Поле {field_selector} имеет tabindex=-1 (недоступно с клавиатуры)"
        assert not is_disabled, f"Поле {field_selector} disabled"
        
        return self
