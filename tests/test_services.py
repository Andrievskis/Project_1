import json
import re

import pytest

from src.services import find_physical_transfers, simple_search


@pytest.fixture
def list_data() -> list[dict]:
    return [
        {"Категория": "Продукты", "Описание": "Покупка продуктов в магазине"},
        {"Категория": "Переводы", "Описание": "Иванов И.И. перевод"},
        {"Категория": "Оплата", "Описание": "Интернет"},
        {"Категория": "Продукты", "Описание": "Овощи и фрукты"},
        {"Категория": "Переводы", "Описание": "Петров П.П. перевод"},
    ]


def test_simple_search_valid_input(list_data: list[dict]) -> None:
    """Тест проверки корректной работы функции поиска по существующей категории."""
    result = simple_search("продукты", list_data)
    assert isinstance(result, str)  # Результат должен быть строкой JSON
    data = json.loads(result)
    assert len(data) > 0  # Должны быть найдены записи
    for item in data:
        assert "продукты" in item["Категория"].lower() or "продукты" in item["Описание"].lower()


def test_simple_search_empty_string(list_data: list[dict]) -> None:
    """Тест проверки обработки пустой строки поиска."""
    result = simple_search("", list_data)
    assert result == []


def test_simple_search_nan(list_data: list[dict]) -> None:
    """Тест проверки обработки несуществующего значения поиска."""
    result = simple_search("nan", list_data)
    assert result == []


def test_simple_search_empty_data() -> None:
    """Тест проверки обработки пустых данных."""
    result = simple_search("поиск", [])
    assert result == []


def test_find_physical_transfers_valid(list_data: list[dict]) -> None:
    """Тест проверки корректной работы поиска физических переводов."""
    result = find_physical_transfers(list_data)
    assert isinstance(result, str)
    data = json.loads(result)
    for item in data:
        assert item["Категория"] == "Переводы"
        assert re.search(r"[А-Яа-я]+\s[А-Яа-я]\.", item["Описание"])


def test_find_physical_transfers_empty_data() -> None:
    """Тест проверки обработки пустых данных."""
    result = find_physical_transfers([])
    assert result == []


def test_find_physical_transfers_no_matches() -> None:
    """Тест проверки обработки данных без подходящих записей."""
    test_data = [{"Категория": "Оплата", "Описание": "Интернет"}, {"Категория": "Переводы", "Описание": "1234567890"}]
    result = find_physical_transfers(test_data)
    assert json.loads(result) == []


def test_find_physical_transfers_performance(list_data: list[dict]) -> None:
    """Тест проверки производительности функции поиска переводов."""
    big_data = list_data * 1000

    result = find_physical_transfers(big_data)
    data = json.loads(result)

    for item in data:
        assert item["Категория"] == "Переводы"
        assert re.search(r"[А-Яа-я]+\s[А-Яа-я]\.", item["Описание"])


def test_test_data_fixture(list_data: list[dict]) -> None:
    """Тест проверки корректности фикстуры с тестовыми данными."""
    assert isinstance(list_data, list)
    for item in list_data:
        assert "Категория" in item
        assert "Описание" in item
        assert isinstance(item["Категория"], str)
        assert isinstance(item["Описание"], str)
