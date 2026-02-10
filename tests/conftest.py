"""Главный conftest для импорта shared-конфигурации"""
# Импортируем все фикстуры и хуки из shared
pytest_plugins = ["tests.shared.conftest"]
