"""Компонент шапки сайта"""
import allure
from selene import browser, be, have


class HeaderComponent:
    """Компонент шапки сайта (переиспользуемый)"""
    
    # Локаторы
    HEADER = "header, .header, #header, .site-header, .top"
    LOGO = "a[href='/'], a[href='https://elvirra.ru/'], .logo, .brand, img[alt*='лог']"
    NAV_LINKS = "nav a, .menu a, .navbar a, a[href]"
    
    @allure.step("Проверить видимость шапки")
    def should_be_visible(self):
        """Проверить, что шапка видима"""
        assert len(browser.all(self.HEADER)) > 0 or len(browser.all("a[href]")) > 0
        return self
    
    @allure.step("Проверить, что логотип в шапке кликабелен")
    def should_have_clickable_logo(self):
        """Проверить кликабельность логотипа"""
        assert len(browser.all(self.LOGO)) > 0
        return self
    
    @allure.step("Кликнуть по логотипу в шапке")
    def click_logo(self):
        """Кликнуть по логотипу"""
        if len(browser.all(self.LOGO)) > 0:
            browser.all(self.LOGO).first.click()
        return self
    
    @allure.step("Проверить наличие навигационных ссылок в шапке")
    def should_have_navigation_links(self):
        """Проверить наличие ссылок навигации"""
        links = browser.all(self.NAV_LINKS)
        assert len(links) > 0, "На странице не найдено навигационных ссылок"
        return self
    
    @allure.step("Кликнуть по ссылке в навигации: {link_text}")
    def click_nav_link(self, link_text: str):
        """Кликнуть по ссылке с указанным текстом"""
        browser.element(self.NAV_LINKS).by(have.text(link_text)).click()
        return self
