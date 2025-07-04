import pandas as pd
import pytest

from src.views import home_page


def test_json_validation() -> None:
    """Тест для проверки валидности JSON."""
    import json

    timestamp = pd.Timestamp("2025-06-30 00:00:00")
    response = home_page(timestamp)
    try:
        json.dumps(response)
    except (TypeError, ValueError) as e:
        pytest.fail(f"Ошибка при сериализации в JSON: {str(e)}")


def test_error_handling() -> None:
    """Тест проверяет корректную обработку ошибок."""
    with pytest.raises(ValueError):
        home_page(pd.Timestamp("некорректный формат"))
