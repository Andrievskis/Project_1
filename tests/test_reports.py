from typing import Any, Dict, List

import pandas as pd
import pytest

from src.reports import report_saver, spending_by_category


@pytest.fixture
def test_dataframe() -> pd.DataFrame:
    """
    Создает фикстуру с тестовыми данными для операций.

    Returns:
        pd.DataFrame: DataFrame с тестовыми данными операций
    """
    data: Dict[str, List[Any]] = {
        "Дата операции": ["20.05.2020", "15.04.2020", "10.03.2020", "05.02.2020"],
        "Категория": ["ЖКХ", "ЖКХ", "Продукты", "ЖКХ"],
        "Сумма": [1000, 1200, 500, 1100],
    }
    return pd.DataFrame(data)


def test_spending_by_category_invalid_category(test_dataframe: pd.DataFrame) -> None:
    """
    Тестирует обработку несуществующей категории.

    Args:
        test_dataframe (pd.DataFrame): тестовые данные операций

    Checks:
        - Возвращает пустой результат при несуществующей категории
    """
    result: List[Dict[str, Any]] = spending_by_category(test_dataframe, "Неправильная категория", "20.05.2020")
    assert len(result) == 0


def test_report_saver() -> None:
    """
    Тестирует работу декоратора report_saver.

    Checks:
        - Функция возвращает корректные данные
        - Результат имеет тип dict
    """

    @report_saver("test_report.json")
    def testing_function() -> Dict[str, str]:
        return {"test": "data"}

    result: Dict[str, str] = testing_function()
    assert result == {"test": "data"}
    assert isinstance(result, dict)


def test_spending_by_category_date_format(test_dataframe: pd.DataFrame) -> None:
    """
    Тестирует форматирование даты в результатах.

    Args:
        test_dataframe (pd.DataFrame): тестовые данные операций

    Checks:
        - Дата форматируется в формате ДД.ММ.ГГГГ
    """
    result: List[Dict[str, Any]] = spending_by_category(test_dataframe, "ЖКХ", "20.05.2020")
    for record in result:
        assert len(record["Дата операции"].split(".")) == 3
