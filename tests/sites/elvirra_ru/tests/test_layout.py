"""Тесты из раздела 'Чек-лист: Вёрстка'"""
import allure
import pytest
from selene import browser
from tests.sites.elvirra_ru.pages.home_page import HomePage


@allure.parent_suite("elvirra.ru")
@allure.suite("Чек-лист: Вёрстка")
@pytest.mark.layout
@pytest.mark.smoke
class TestLayout:
    """Тесты вёрстки сайта"""
    
    @allure.sub_suite("Сайт имеет favicon.")
    @allure.title("Проверка наличия favicon")
    @allure.description("Проверяем, что на сайте присутствует favicon")
    def test_site_has_favicon(self):
        """Сайт должен иметь favicon"""
        home = HomePage()
        
        home.open_home()
        home.should_have_favicon()
    
    @allure.sub_suite("В консоли браузера отсутствуют ошибки JavaScript.")
    @allure.title("Проверка отсутствия JS ошибок в консоли")
    @allure.description("Проверяем, что в консоли браузера нет критических JS ошибок")
    def test_no_js_errors_in_console(self):
        """В консоли не должно быть JS ошибок"""
        home = HomePage()
        
        home.open_home()
        home.should_have_no_js_errors()
    
    @allure.sub_suite("Используется кодировка UTF-8.")
    @allure.title("Проверка кодировки UTF-8")
    @allure.description("Проверяем, что страница использует UTF-8")
    def test_utf8_encoding(self):
        """Страница должна использовать кодировку UTF-8"""
        home = HomePage()
        
        home.open_home()
        
        # Получаем кодировку из meta-тега или из заголовков
        encoding_meta = browser.driver().find_elements_by_css_selector(
            'meta[charset], meta[http-equiv="Content-Type"]'
        )

        if len(encoding_meta) > 0:
            # Проверяем первый найденный meta-тег
            first_meta = encoding_meta[0]
            charset = first_meta.get_attribute("charset")

            if not charset:
                content = first_meta.get_attribute("content")
                if content and "utf-8" in content.lower():
                    charset = "UTF-8"
            
            allure.attach(
                f"Найденная кодировка: {charset}",
                name="Кодировка страницы",
                attachment_type=allure.attachment_type.TEXT
            )
            
            if charset:
                assert "utf-8" in charset.lower(), f"Кодировка не UTF-8: {charset}"
        else:
            allure.attach(
                "Meta-тег с кодировкой не найден, предполагаем UTF-8 по умолчанию",
                name="Информация о кодировке",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @allure.sub_suite("Шрифты успешно загружаются и корректно отображаются.")
    @allure.title("Проверка загрузки шрифтов")
    @allure.description("Базовая проверка отображения текста на странице")
    def test_fonts_load_correctly(self):
        """Шрифты должны загружаться корректно"""
        home = HomePage()
        
        home.open_home()
        
        # Базовая проверка: текст на странице отображается
        body_text = browser.element("body").text
        
        assert len(body_text) > 0, "На странице нет текстового контента"
        
        allure.attach(
            f"Длина текста на странице: {len(body_text)} символов",
            name="Текстовый контент",
            attachment_type=allure.attachment_type.TEXT
        )
    
    @allure.sub_suite("Элементы веб-страниц корректно отображаются на разных разрешениях экрана.")
    @allure.title("Проверка отображения на разных разрешениях (Desktop)")
    @allure.description("Проверяем корректность отображения на стандартном разрешении")
    def test_responsive_desktop(self):
        """Сайт должен корректно отображаться на desktop разрешении"""
        home = HomePage()
        
        # Desktop разрешение (1920x1080)
        browser.driver().set_window_size(1920, 1080)
        
        home.open_home()
        home.should_have_header()
        home.should_have_main_content()
        home.should_have_footer()
    
    @allure.sub_suite("Элементы веб-страниц корректно отображаются на разных разрешениях экрана.")
    @allure.title("Проверка отображения на разных разрешениях (Tablet)")
    @allure.description("Проверяем корректность отображения на планшетном разрешении")
    def test_responsive_tablet(self):
        """Сайт должен корректно отображаться на tablet разрешении"""
        home = HomePage()
        
        # Tablet разрешение (768x1024)
        browser.driver().set_window_size(768, 1024)
        
        home.open_home()
        home.should_have_header()
        home.should_have_main_content()
        home.should_have_footer()
    
    @allure.sub_suite("Элементы веб-страниц корректно отображаются на разных разрешениях экрана.")
    @allure.title("Проверка отображения на разных разрешениях (Mobile)")
    @allure.description("Проверяем корректность отображения на мобильном разрешении")
    def test_responsive_mobile(self):
        """Сайт должен корректно отображаться на mobile разрешении"""
        home = HomePage()
        
        # Mobile разрешение (375x667)
        browser.driver().set_window_size(375, 667)
        
        home.open_home()
        home.should_have_header()
        home.should_have_main_content()
    
    @allure.sub_suite("Функциональность кнопок подтверждена на различных страницах.")
    @allure.title("Проверка функциональности кнопок")
    @allure.description("Проверяем, что кнопки кликабельны")
    def test_buttons_functionality(self):
        """Кнопки должны быть функциональны"""
        home = HomePage()
        
        home.open_home()
        home.should_have_clickable_buttons()
    
    @allure.sub_suite("Вёрстка форм корректно адаптируется при изменении размеров окна.")
    @allure.title("Проверка адаптивности форм")
    @allure.description("Проверяем отображение страницы при изменении размера окна")
    def test_forms_responsive(self):
        """Формы должны адаптироваться при изменении размера окна"""
        home = HomePage()
        
        # Открываем на desktop
        browser.driver().set_window_size(1920, 1080)
        home.open_home()
        home.should_have_main_content()
        
        # Меняем на mobile
        browser.driver().set_window_size(375, 667)
        
        # Проверяем, что контент всё ещё виден
        home.should_have_main_content()
