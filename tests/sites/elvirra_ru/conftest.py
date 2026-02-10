"""Конфигурация для тестов elvirra.ru"""
import pytest
from tests.sites.elvirra_ru.data.urls import BASE_URL


@pytest.fixture(scope="session")
def base_url():
    """Базовый URL для сайта elvirra.ru"""
    return BASE_URL
