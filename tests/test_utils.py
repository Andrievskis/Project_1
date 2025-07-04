from typing import Any
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.utils import (
    get_currency_data,
    get_price_stock,
    information_for_each_card,
    read_excel,
    top_five_transactions,
    welcome_function,
)


def test_read_excel_success(monkeypatch: Any) -> None:
    """Тест успешной работы функции read_excel. Проверяет корректность чтения Excel файла
    и преобразования данных в словарь."""
    test_info = pd.DataFrame(
        {"date": ["2023-01-01", "2023-01-02"], "amount": [100, 200], "type": ["income", "expense"]}
    )
    monkeypatch.setattr("pandas.read_excel", Mock(return_value=test_info))

    result = read_excel("test_path.xlsx")
    expected = test_info.to_dict(orient="records")

    assert result == expected


def test_read_excel_file_not_found() -> None:
    """Тест обработки ошибки при отсутствии файла. Проверяет логирование ошибки
    и возврат строкового сообщения."""
    with patch("logging.Logger.error") as mock_logger:
        result = read_excel("non_existent_file.xlsx")
        mock_logger.assert_called()
        assert isinstance(result, str)


def test_read_excel_exception() -> None:
    """Тест обработки исключений при чтении Excel. Проверяет логирование ошибки
    и возврат сообщения с текстом исключения."""
    with patch("pandas.read_excel", side_effect=Exception("Test exception")):
        with patch("logging.Logger.error") as mock_logger:
            result = read_excel("test_path.xlsx")
            mock_logger.assert_called()
            assert isinstance(result, str)
            assert "Test exception" in result


def test_day_time_now() -> None:
    """Тест функции приветствия в зависимости от времени суток. Проверяет корректность
    определения времени суток и соответствующего приветствия."""
    current_hour = pd.Timestamp.now().hour
    greeting = welcome_function()

    if 0 <= current_hour < 6 or 22 <= current_hour <= 23:
        assert greeting == "Доброй ночи"
    elif 17 <= current_hour <= 22:
        assert greeting == "Добрый вечер"
    elif 7 <= current_hour <= 11:
        assert greeting == "Доброе утро"
    else:
        assert greeting == "Добрый день"


@patch("pandas.read_excel")
def test_information_for_each_card_success(mock_read_excel: Any) -> None:
    """Тест успешной работы функции information_for_each_card. Проверяет корректность
    обработки данных по картам."""
    test_info_card = pd.DataFrame(
        {
            "Дата операции": ["01.09.2018 00:00:00", "02.09.2018 00:00:00"],
            "Номер карты": ["1234567890123456", "1234567890123456"],
            "Сумма операции с округлением": [1000, 2000],
        }
    )

    mock_read_excel.return_value = test_info_card

    result = information_for_each_card(pd.to_datetime("29-09-2018 00:00:00", dayfirst=True))

    expected = [{"last_digits": "3456", "total_spent": 3000.00, "cashback": 30.00}]

    assert result == expected


def test_information_for_each_card_exception() -> None:
    """Тест проверки обработки исключений в функции information_for_each_card. Проверяет корректность
    логирования ошибки, возврат строкового сообщения с текстом исключения."""
    with patch("pandas.read_excel", side_effect=Exception("Test exception")):
        with patch("logging.Logger.error") as mock_logger:
            result = information_for_each_card(pd.to_datetime("29-09-2018 00:00:00", dayfirst=True))
            mock_logger.assert_called()
            assert isinstance(result, str)
            assert "Test exception" in result


test_data_for_operation_cards = {
    "Дата операции": [
        "01.06.2025 12:00:00",
        "02.06.2025 13:00:00",
        "03.06.2025 14:00:00",
        "04.06.2025 15:00:00",
        "05.06.2025 16:00:00",
        "06.06.2025 17:00:00",
    ],
    "Сумма операции с округлением": [1000, 500, 2000, 1500, 2500, 3000],
    "Категория": ["Покупка", "Перевод", "Покупка", "Перевод", "Покупка", "Перевод"],
    "Описание": ["Тест1", "Тест2", "Тест3", "Тест4", "Тест5", "Тест6"],
}


@pytest.fixture
def mock_excel_data() -> Any:
    """Фикстура для создания тестового DataFrame с данными Excel.
    Возвращает: DataFrame с преобразованными датами."""
    df = pd.DataFrame(test_data_for_operation_cards)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    return df


@patch("pandas.read_excel")
def test_top_five_transactions(mock_read_excel: Any, mock_excel_data: Any) -> None:
    """Тестирует функцию получения топ-5 транзакций. Параметры: mock_read_excel (Mock):
    Мок для pandas.read_excel mock_excel_data (pd.DataFrame): Фиктивные данные Excel."""
    mock_read_excel.return_value = mock_excel_data

    test_date = pd.Timestamp("2025-06-30")

    result = top_five_transactions(test_date)

    expected_result = [
        {"date": "06.06.2025", "amount": 3000.00, "category": "Перевод", "description": "Тест6"},
        {"date": "05.06.2025", "amount": 2500.00, "category": "Покупка", "description": "Тест5"},
        {"date": "03.06.2025", "amount": 2000.00, "category": "Покупка", "description": "Тест3"},
        {"date": "04.06.2025", "amount": 1500.00, "category": "Перевод", "description": "Тест4"},
        {"date": "01.06.2025", "amount": 1000.00, "category": "Покупка", "description": "Тест1"},
    ]

    assert result == expected_result


TEST_USER_SETTINGS = {"user_currencies": ["USD", "EUR"]}

TEST_API_RESPONSE = {"conversion_rates": {"RUB": 75.00}}

MOCK_CURRENCY_DATA = {"USD": {"conversion_rates": {"RUB": 90.0}}, "EUR": {"conversion_rates": {"RUB": 98.5}}}

MOCK_STOCK_DATA = {
    "AAPL": {"Global Quote": {"05. price": "150.75"}},
    "MSFT": {"Global Quote": {"05. price": "300.25"}},
}


def mock_currency_request(url: str) -> Any:
    """Создает мок-ответ для запросов курсов валют."""
    currency = url.split("/")[-1]
    response = type("Response", (object,), {"status_code": 200, "json": lambda: MOCK_CURRENCY_DATA[currency]})()
    return response


def mock_stock_request(url: str) -> Any:
    """Создает мок-ответ для запросов цен акций."""
    stock = url.split("=")[-1]
    response = type(
        "Response", (object,), {"status_code": 200, "json": lambda: {"Global Quote": MOCK_STOCK_DATA[stock]}}
    )()
    return response


def test_get_currency_data_error() -> None:
    """Тестирует обработку ошибок в функции получения курсов валют."""
    with patch("builtins.open", side_effect=FileNotFoundError), patch("requests.get", side_effect=Exception):
        result = get_currency_data()
        assert isinstance(result, str)
        assert "Произошла ошибка" in result


def test_get_price_stock_error() -> None:
    """Тестирует обработку ошибок в функции получения цен акций."""
    with patch("builtins.open", side_effect=FileNotFoundError), patch("requests.get", side_effect=Exception):
        result = get_price_stock()
        assert isinstance(result, str)
        assert "Произошла ошибка" in result
