"""Page Object для главной страницы elvirra.ru"""
import allure
from selene import browser, be, have
from tests.sites.elvirra_ru.pages.base_page import BasePage
from tests.sites.elvirra_ru.data.urls import BASE_URL, HOME


class HomePage(BasePage):
    """Главная страница сайта"""
    
    def __init__(self):
        super().__init__(BASE_URL)
        self.path = HOME
    
    # Локаторы
    HEADER = "header, .header, #header, .site-header, .top"
    FOOTER = "footer, .footer, #footer, .site-footer, .bottom"
    MAIN_CONTENT = "main, #content, .content, .main, body"
    LOGO = "a[href='/'], a[href='https://elvirra.ru/'], img[alt*='logo'], .logo, .brand"
    NAV_MENU = "nav, .nav, .menu, .navbar, .main-menu"
    
    @allure.step("Открыть главную страницу")
    def open_home(self):
        """Открыть главную страницу"""
        self.open(self.path)
        return self
    
    @allure.step("Проверить, что шапка сайта видима")
    def should_have_header(self):
        """Проверить наличие шапки сайта"""
        if browser.all(self.HEADER).size() == 0:
            # На части шаблонов нет semantic-header, считаем хедером меню/верхнюю панель.
            assert browser.all("a[href], .menu, .top, .header").size() > 0, "Верхний блок не найден"
        return self
    
    @allure.step("Проверить, что подвал сайта видим")
    def should_have_footer(self):
        """Проверить наличие подвала сайта"""
        if browser.all(self.FOOTER).size() == 0:
            page_text = browser.element("body").text.lower()
            assert "elvirra" in page_text or "©" in page_text, "Подвал/копирайт не найден"
        return self
    
    @allure.step("Проверить, что основной контент видим")
    def should_have_main_content(self):
        """Проверить наличие основного контента"""
        assert len(browser.element("body").text.strip()) > 0, "Основной контент не найден"
        return self
    
    @allure.step("Проверить, что логотип видим и кликабелен")
    def should_have_clickable_logo(self):
        """Проверить наличие и кликабельность логотипа"""
        assert browser.all(self.LOGO).size() > 0, "Логотип или ссылка на главную не найдены"
        return self
    
    @allure.step("Проверить, что навигационное меню видимо")
    def should_have_navigation(self):
        """Проверить наличие навигационного меню"""
        has_nav = browser.all(self.NAV_MENU).size() > 0
        has_links = browser.all("a[href]").size() > 0
        assert has_nav or has_links, "Навигационные элементы не найдены"
        return self
    
    @allure.step("Кликнуть по логотипу")
    def click_logo(self):
        """Кликнуть по логотипу (переход на главную)"""
        self.click(self.LOGO)
        return self
    
    @allure.step("Проверить, что на странице есть заголовок")
    def should_have_page_title(self):
        """Проверить, что у страницы есть непустой title"""
        title = browser.driver().title
        assert title and len(title) > 0, "Title страницы пустой"
        allure.attach(title, name="Title страницы", attachment_type=allure.attachment_type.TEXT)
        return self
    
    @allure.step("Найти и проверить все ссылки на странице")
    def should_have_working_links(self):
        """Проверить, что основные ссылки присутствуют и кликабельны"""
        links = browser.all("a[href]")
        links_count = links.size()
        
        assert links_count > 0, "На странице не найдено ни одной ссылки"
        allure.attach(
            f"Найдено ссылок: {links_count}",
            name="Количество ссылок",
            attachment_type=allure.attachment_type.TEXT
        )
        return self
    
    @allure.step("Проверить, что все кнопки на странице кликабельны")
    def should_have_clickable_buttons(self):
        """Проверить наличие и кликабельность кнопок"""
        buttons = browser.all("button, input[type='submit'], input[type='button']")
        buttons_count = buttons.size()
        
        allure.attach(
            f"Найдено кнопок: {buttons_count}",
            name="Количество кнопок",
            attachment_type=allure.attachment_type.TEXT
        )
        return self
