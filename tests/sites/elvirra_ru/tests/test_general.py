"""Тесты из раздела 'Чек-лист: Общее'"""
import allure
import pytest
from tests.sites.elvirra_ru.pages.home_page import HomePage
from tests.sites.elvirra_ru.components.header_component import HeaderComponent


@allure.parent_suite("elvirra.ru")
@allure.suite("Чек-лист: Общее")
@pytest.mark.general
@pytest.mark.smoke
class TestGeneral:
    """Тесты общей функциональности сайта"""
    
    @allure.sub_suite("Сайт корректно открывается и доступен.")
    @allure.title("Проверка доступности сайта")
    @allure.description("Проверяем, что сайт открывается и основные элементы видимы")
    def test_site_is_accessible(self):
        """Сайт должен открываться и быть доступным"""
        home = HomePage()
        
        home.open_home()
        home.should_have_header()
        home.should_have_main_content()
        home.should_have_footer()
    
    @allure.sub_suite("Повторное открытие сайта выполняется без сбоев.")
    @allure.title("Проверка повторного открытия сайта")
    @allure.description("Проверяем, что сайт можно открыть повторно без ошибок")
    def test_site_reopens_without_errors(self):
        """Сайт должен открываться повторно без сбоев"""
        home = HomePage()
        
        # Первое открытие
        home.open_home()
        home.should_have_header()
        
        # Повторное открытие
        home.open_home()
        home.should_have_header()
        home.should_have_main_content()
    
    @allure.sub_suite("Все кнопки на сайте реагируют на нажатие.")
    @allure.title("Проверка кликабельности кнопок")
    @allure.description("Проверяем, что кнопки на странице кликабельны")
    def test_buttons_are_clickable(self):
        """Все кнопки должны быть кликабельны"""
        home = HomePage()
        
        home.open_home()
        home.should_have_clickable_buttons()
    
    @allure.sub_suite("Все ссылки переходят на соответствующие страницы.")
    @allure.title("Проверка наличия ссылок")
    @allure.description("Проверяем, что на странице есть рабочие ссылки")
    def test_links_are_present(self):
        """Ссылки должны присутствовать на странице"""
        home = HomePage()
        
        home.open_home()
        home.should_have_working_links()
    
    @allure.sub_suite("Основные элементы сайта функционируют без нарушений.")
    @allure.title("Проверка основных элементов сайта")
    @allure.description("Проверяем работоспособность основных элементов: шапка, контент, подвал")
    def test_main_elements_work(self):
        """Основные элементы сайта должны функционировать"""
        home = HomePage()
        
        home.open_home()
        home.should_have_header()
        home.should_have_main_content()
        home.should_have_footer()
        home.should_have_navigation()
    
    @allure.sub_suite("Навигационное меню работает корректно.")
    @allure.title("Проверка навигационного меню")
    @allure.description("Проверяем наличие и видимость навигационного меню")
    def test_navigation_menu_works(self):
        """Навигационное меню должно работать корректно"""
        home = HomePage()
        header = HeaderComponent()
        
        home.open_home()
        home.should_have_navigation()
        header.should_have_navigation_links()
    
    @allure.sub_suite("На всех страницах присутствует ссылка на домашнюю страницу.")
    @allure.title("Проверка ссылки на главную страницу (логотип)")
    @allure.description("Проверяем, что логотип кликабелен и ведёт на главную")
    def test_home_link_present(self):
        """На странице должна быть ссылка на главную (логотип)"""
        home = HomePage()
        
        home.open_home()
        home.should_have_clickable_logo()
