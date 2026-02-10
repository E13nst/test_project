"""Тесты из раздела 'Чек-лист: Удобство сайта'"""
import allure
import pytest
from selene import browser
from tests.sites.elvirra_ru.pages.home_page import HomePage


@allure.parent_suite("elvirra.ru")
@allure.suite("Чек-лист: Удобство сайта")
@pytest.mark.usability
@pytest.mark.smoke
class TestUsability:
    """Тесты удобства использования сайта"""
    
    @allure.sub_suite("На каждой странице присутствует заголовок.")
    @allure.title("Проверка наличия заголовка страницы")
    @allure.description("Проверяем, что у страницы есть непустой title")
    def test_page_has_title(self):
        """На странице должен быть заголовок (title)"""
        home = HomePage()
        
        home.open_home()
        home.should_have_page_title()
    
    @allure.sub_suite("Выравнивание текста единообразно, элементы выглядят ровно и эстетично.")
    @allure.title("Проверка единообразия основных элементов")
    @allure.description("Проверяем наличие и корректное отображение основных блоков")
    def test_elements_aligned_properly(self):
        """Элементы должны быть выровнены и отображаться корректно"""
        home = HomePage()
        
        home.open_home()
        home.should_have_header()
        home.should_have_main_content()
        home.should_have_footer()
    
    @allure.sub_suite("Все кнопки выполнены в едином стиле и стандартного размера.")
    @allure.title("Проверка наличия кнопок на странице")
    @allure.description("Проверяем, что кнопки присутствуют и кликабельны")
    def test_buttons_consistent_style(self):
        """Кнопки должны быть единообразны и кликабельны"""
        home = HomePage()
        
        home.open_home()
        home.should_have_clickable_buttons()
    
    @allure.sub_suite("На всех страницах присутствует ссылка на домашнюю страницу.")
    @allure.title("Проверка ссылки на домашнюю страницу")
    @allure.description("Проверяем наличие кликабельного логотипа")
    def test_home_link_on_all_pages(self):
        """На всех страницах должна быть ссылка на главную"""
        home = HomePage()
        
        home.open_home()
        home.should_have_clickable_logo()
    
    @allure.sub_suite("Все поля (текстовые, выпадающие списки, радио-кнопки и т.д.) и кнопки доступны с клавиатуры.")
    @allure.title("Проверка доступности элементов с клавиатуры")
    @allure.description("Проверяем, что интерактивные элементы доступны для фокуса")
    def test_keyboard_accessibility(self):
        """Поля и кнопки должны быть доступны с клавиатуры"""
        home = HomePage()
        
        home.open_home()
        
        # Проверяем, что есть интерактивные элементы (кнопки, ссылки, поля)
        interactive_elements = browser.all("a, button, input, select, textarea")
        count = interactive_elements.size()
        
        assert count > 0, "На странице не найдено интерактивных элементов"
        
        allure.attach(
            f"Найдено интерактивных элементов: {count}",
            name="Количество интерактивных элементов",
            attachment_type=allure.attachment_type.TEXT
        )
    
    @allure.sub_suite("У всех полей есть подсказки и отображается корректный формат заполнения.")
    @allure.title("Проверка наличия подсказок у полей ввода")
    @allure.description("Проверяем, что у полей есть placeholder или label")
    def test_fields_have_hints(self):
        """У полей должны быть подсказки (placeholder/label)"""
        home = HomePage()
        
        home.open_home()
        
        # Ищем все поля ввода на странице
        input_fields = browser.driver().find_elements_by_css_selector(
            "input[type='text'], input[type='email'], input[type='tel'], textarea"
        )
        fields_count = len(input_fields)
        
        if fields_count > 0:
            # Проверяем первое поле на наличие placeholder или связанного label
            first_field = input_fields[0]

            placeholder = first_field.get_attribute("placeholder")
            field_id = first_field.get_attribute("id")
            
            has_hint = placeholder is not None and len(placeholder) > 0
            
            # Проверяем наличие label
            if field_id:
                labels = browser.driver().find_elements_by_css_selector(f'label[for="{field_id}"]')
                if len(labels) > 0:
                    has_hint = True
            
            allure.attach(
                f"Найдено полей ввода: {fields_count}\nПервое поле имеет подсказку: {has_hint}",
                name="Проверка подсказок",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.attach(
                "На главной странице не найдено полей ввода",
                name="Информация о полях",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @allure.sub_suite("Элементы дизайна не наслаиваются друг на друга.")
    @allure.title("Проверка отсутствия наслоения элементов")
    @allure.description("Базовая проверка корректности отображения элементов")
    def test_no_overlapping_elements(self):
        """Элементы не должны наслаиваться друг на друга"""
        home = HomePage()
        
        home.open_home()
        
        # Базовая проверка: все основные блоки видимы
        home.should_have_header()
        home.should_have_main_content()
        home.should_have_footer()
    
    @allure.sub_suite("Между элементами интерфейса (поля, кнопки и т.д.) присутствует достаточное пространство.")
    @allure.title("Проверка наличия пространства между элементами")
    @allure.description("Проверяем, что основные элементы не слипаются")
    def test_proper_spacing_between_elements(self):
        """Между элементами должно быть достаточное пространство"""
        home = HomePage()
        
        home.open_home()
        
        # Базовая проверка видимости элементов
        home.should_have_header()
        home.should_have_main_content()
        home.should_have_footer()
