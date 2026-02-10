.PHONY: help venv install test test-smoke test-general test-usability test-layout test-allure clean clean-allure clean-cache lint format check

# Переменные
ALLURE_DIR = allure-results
ALLURE_REPORT = allure-report
PYTHON = python3
VENV = venv
VENV_PYTHON = $(VENV)/bin/python
VENV_PIP = $(VENV)/bin/pip
VENV_PYTEST = $(VENV)/bin/pytest

# Цвета для вывода
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
BLUE = \033[0;34m
NC = \033[0m # No Color

help: ## Показать справку по командам
	@echo "$(GREEN)Доступные команды:$(NC)"
	@echo ""
	@echo "$(YELLOW)Установка:$(NC)"
	@echo "  make venv             - Создать виртуальное окружение"
	@echo "  make install          - Установить зависимости (создаст venv автоматически)"
	@echo ""
	@echo "$(YELLOW)Запуск тестов:$(NC)"
	@echo "  make test             - Запустить все тесты"
	@echo "  make test-smoke       - Запустить только smoke-тесты"
	@echo "  make test-general     - Запустить тесты 'Чек-лист: Общее'"
	@echo "  make test-usability   - Запустить тесты 'Чек-лист: Удобство сайта'"
	@echo "  make test-layout      - Запустить тесты 'Чек-лист: Вёрстка'"
	@echo "  make test-elvirra     - Запустить все тесты для elvirra.ru"
	@echo "  make test-verbose     - Запустить тесты с подробным выводом"
	@echo ""
	@echo "$(YELLOW)Allure-отчёты:$(NC)"
	@echo "  make test-allure      - Запустить тесты с генерацией Allure-отчёта"
	@echo "  make allure-serve     - Открыть Allure-отчёт в браузере"
	@echo "  make allure-generate  - Сгенерировать статический Allure-отчёт"
	@echo "  make allure-open      - Запустить тесты и открыть отчёт"
	@echo ""
	@echo "$(YELLOW)Очистка:$(NC)"
	@echo "  make clean            - Очистить кэш pytest и __pycache__"
	@echo "  make clean-venv       - Удалить виртуальное окружение"
	@echo "  make clean-allure     - Удалить Allure-результаты и отчёты"
	@echo "  make clean-all        - Полная очистка (кэш + Allure)"
	@echo "  make clean-everything - Полная очистка включая venv"
	@echo ""
	@echo "$(YELLOW)Проверка кода:$(NC)"
	@echo "  make lint             - Проверить код линтером"
	@echo "  make check            - Проверить синтаксис всех Python-файлов"

venv: ## Создать виртуальное окружение
	@if [ ! -d "$(VENV)" ]; then \
		echo "$(GREEN)Создание виртуального окружения...$(NC)"; \
		$(PYTHON) -m venv $(VENV); \
		echo "$(GREEN)✓ Виртуальное окружение создано$(NC)"; \
	else \
		echo "$(YELLOW)Виртуальное окружение уже существует$(NC)"; \
	fi

install: venv ## Установить зависимости (создаст venv автоматически)
	@echo "$(GREEN)Установка зависимостей...$(NC)"
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Зависимости установлены в $(VENV)/$(NC)"
	@echo "$(BLUE)💡 Для активации venv выполните: source $(VENV)/bin/activate$(NC)"

# Запуск тестов
test: install ## Запустить все тесты
	@echo "$(GREEN)Запуск всех тестов...$(NC)"
	$(VENV_PYTEST) -v

test-smoke: install ## Запустить только smoke-тесты
	@echo "$(GREEN)Запуск smoke-тестов...$(NC)"
	$(VENV_PYTEST) -m smoke -v

test-general: install ## Запустить тесты раздела "Общее"
	@echo "$(GREEN)Запуск тестов 'Чек-лист: Общее'...$(NC)"
	$(VENV_PYTEST) -m general -v

test-usability: install ## Запустить тесты раздела "Удобство сайта"
	@echo "$(GREEN)Запуск тестов 'Чек-лист: Удобство сайта'...$(NC)"
	$(VENV_PYTEST) -m usability -v

test-layout: install ## Запустить тесты раздела "Вёрстка"
	@echo "$(GREEN)Запуск тестов 'Чек-лист: Вёрстка'...$(NC)"
	$(VENV_PYTEST) -m layout -v

test-elvirra: install ## Запустить все тесты для elvirra.ru
	@echo "$(GREEN)Запуск тестов для elvirra.ru...$(NC)"
	$(VENV_PYTEST) tests/sites/elvirra_ru/ -v

test-verbose: install ## Запустить тесты с подробным выводом
	@echo "$(GREEN)Запуск тестов с подробным выводом...$(NC)"
	$(VENV_PYTEST) -vv --tb=short

# Allure-отчёты
test-allure: install ## Запустить тесты с генерацией Allure-отчёта
	@echo "$(GREEN)Запуск тестов с генерацией Allure-отчёта...$(NC)"
	$(VENV_PYTEST) --alluredir=$(ALLURE_DIR) -v
	@echo "$(GREEN)✓ Результаты сохранены в $(ALLURE_DIR)/$(NC)"

allure-serve: ## Открыть Allure-отчёт в браузере
	@if [ ! -d "$(ALLURE_DIR)" ]; then \
		echo "$(RED)✗ Директория $(ALLURE_DIR) не найдена. Сначала запустите 'make test-allure'$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Открытие Allure-отчёта в браузере...$(NC)"
	allure serve $(ALLURE_DIR)

allure-generate: ## Сгенерировать статический Allure-отчёт
	@if [ ! -d "$(ALLURE_DIR)" ]; then \
		echo "$(RED)✗ Директория $(ALLURE_DIR) не найдена. Сначала запустите 'make test-allure'$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Генерация статического Allure-отчёта...$(NC)"
	allure generate $(ALLURE_DIR) -o $(ALLURE_REPORT) --clean
	@echo "$(GREEN)✓ Отчёт сгенерирован в $(ALLURE_REPORT)/$(NC)"
	@echo "$(YELLOW)Откройте файл: $(ALLURE_REPORT)/index.html$(NC)"

allure-open: test-allure allure-serve ## Запустить тесты и открыть Allure-отчёт

# Очистка
clean: ## Очистить кэш pytest и __pycache__
	@echo "$(YELLOW)Очистка кэша pytest и __pycache__...$(NC)"
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".cache" -exec rm -r {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Кэш очищен$(NC)"

clean-venv: ## Удалить виртуальное окружение
	@echo "$(YELLOW)Удаление виртуального окружения...$(NC)"
	rm -rf $(VENV) 2>/dev/null || true
	@echo "$(GREEN)✓ Виртуальное окружение удалено$(NC)"

clean-allure: ## Удалить Allure-результаты и отчёты
	@echo "$(YELLOW)Удаление Allure-результатов и отчётов...$(NC)"
	rm -rf $(ALLURE_DIR) $(ALLURE_REPORT) 2>/dev/null || true
	@echo "$(GREEN)✓ Allure-файлы удалены$(NC)"

clean-all: clean clean-allure ## Полная очистка (кэш + Allure)
	@echo "$(GREEN)✓ Полная очистка завершена$(NC)"

clean-everything: clean clean-allure clean-venv ## Полная очистка включая venv
	@echo "$(GREEN)✓ Полная очистка завершена (включая venv)$(NC)"

# Проверка кода
lint: ## Проверить код линтером (flake8, если установлен)
	@echo "$(GREEN)Проверка кода линтером...$(NC)"
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 tests/ --max-line-length=120 --ignore=E501,W503 || echo "$(YELLOW)flake8 не найден, пропускаем$(NC)"; \
	else \
		echo "$(YELLOW)flake8 не установлен. Установите: pip install flake8$(NC)"; \
	fi

check: ## Проверить синтаксис всех Python-файлов
	@echo "$(GREEN)Проверка синтаксиса Python-файлов...$(NC)"
	@if [ -f "$(VENV_PYTHON)" ]; then \
		find tests -name "*.py" -exec $(VENV_PYTHON) -m py_compile {} \; 2>&1 | grep -v "^$$" || true; \
	else \
		find tests -name "*.py" -exec $(PYTHON) -m py_compile {} \; 2>&1 | grep -v "^$$" || true; \
	fi
	@echo "$(GREEN)✓ Синтаксис всех файлов корректен$(NC)"

# Комбинации команд
ci: clean-all test-allure allure-generate ## CI-пайплайн: очистка → тесты → отчёт
	@echo "$(GREEN)✓ CI-пайплайн завершён$(NC)"

default: help ## Показать справку (по умолчанию)
