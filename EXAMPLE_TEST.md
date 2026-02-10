# Пример теста с полной аннотацией

Этот документ показывает, как правильно писать тесты в рамках фреймворка.

## Полный пример теста

```python
import allure
import pytest
from tests.sites.elvirra_ru.pages.home_page import HomePage


@allure.parent_suite("elvirra.ru")  # 1️⃣ Название сайта
@allure.suite("Чек-лист: Общее")    # 2️⃣ Раздел из CHECKLIST.md
@pytest.mark.general                 # 3️⃣ Маркер для фильтрации
@pytest.mark.smoke                   # 4️⃣ Smoke-тест
class TestGeneral:
    """Тесты общей функциональности сайта"""
    
    @allure.sub_suite("Сайт корректно открывается и доступен.")  # 5️⃣ Пункт из чек-листа
    @allure.title("Проверка доступности сайта")                  # 6️⃣ Краткое название
    @allure.description("Проверяем, что сайт открывается и основные элементы видимы")  # 7️⃣ Описание
    def test_site_is_accessible(self):
        """Сайт должен открываться и быть доступным"""
        # Arrange (подготовка)
        home = HomePage()
        
        # Act (действие)
        home.open_home()
        
        # Assert (проверка)
        home.should_have_header()
        home.should_have_main_content()
        home.should_have_footer()
```

## Структура Allure-иерархии

```
elvirra.ru (parent_suite)
└── Чек-лист: Общее (suite)
    └── Сайт корректно открывается и доступен. (sub_suite)
        └── Проверка доступности сайта (title)
```

## Page Object пример

```python
import allure
from selene import browser, be
from tests.sites.elvirra_ru.pages.base_page import BasePage


class HomePage(BasePage):
    """Главная страница сайта"""
    
    # Локаторы
    HEADER = "header"
    MAIN_CONTENT = "main"
    FOOTER = "footer"
    
    @allure.step("Открыть главную страницу")  # 📝 Шаг в Allure
    def open_home(self):
        """Открыть главную страницу"""
        self.open("/")
        return self  # ✅ Возвращаем self для chaining
    
    @allure.step("Проверить, что шапка сайта видима")
    def should_have_header(self):
        """Проверить наличие шапки сайта"""
        browser.element(self.HEADER).should(be.visible)  # 🔄 Автоожидание
        return self
```

## Ключевые принципы

### 1. Иерархия Allure (обязательно)
- `@allure.parent_suite()` — название сайта
- `@allure.suite()` — раздел чек-листа (точное название)
- `@allure.sub_suite()` — пункт чек-листа (точный текст)

### 2. Маркеры pytest
- `@pytest.mark.smoke` — для smoke-тестов
- `@pytest.mark.general` / `usability` / `layout` — по разделам

### 3. Page Object
- Локаторы — константы класса
- Методы — с `@allure.step()`
- Возвращают `self` для chaining
- Используют автоожидания Selene

### 4. Автоожидания
```python
# ✅ Правильно (с автоожиданием)
browser.element(selector).should(be.visible)
browser.element(selector).should(be.clickable).click()

# ❌ Неправильно (без ожидания)
import time
time.sleep(5)  # Никогда не используйте sleep!
```

### 5. Структура теста (AAA)
```python
def test_example(self):
    # Arrange — подготовка
    page = HomePage()
    
    # Act — действие
    page.open_home()
    
    # Assert — проверка
    page.should_have_header()
```

## Запуск примера

```bash
# Запустить все тесты класса
pytest tests/sites/elvirra_ru/tests/test_general.py::TestGeneral -v

# Запустить конкретный тест
pytest tests/sites/elvirra_ru/tests/test_general.py::TestGeneral::test_site_is_accessible -v

# С Allure-отчётом
pytest tests/sites/elvirra_ru/tests/test_general.py --alluredir=allure-results
allure serve allure-results
```

## Что будет в Allure-отчёте

### Успешный тест
- ✅ Зелёная галочка
- 📊 Время выполнения
- 📝 Все шаги (`@allure.step`)
- 🏷️ Группировка по parent_suite → suite → sub_suite

### Упавший тест
- ❌ Красный крестик
- 📸 Скриншот страницы
- 📄 HTML-код страницы
- 🔗 URL страницы
- 📝 Traceback ошибки
- 📊 Все шаги до падения

## Добавление нового теста

1. Определите пункт из CHECKLIST.md
2. Выберите правильный раздел (Общее/Удобство/Вёрстка)
3. Создайте тест с правильными декораторами
4. Используйте существующие Page Object или создайте новые
5. Запустите и проверьте в Allure

Пример:
```python
@allure.parent_suite("elvirra.ru")
@allure.suite("Чек-лист: Вёрстка")
@allure.sub_suite("Сайт имеет favicon.")
@pytest.mark.layout
def test_favicon_exists(self):
    home = HomePage()
    home.open_home()
    home.should_have_favicon()
```
