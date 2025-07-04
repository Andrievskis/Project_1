import json
from typing import Any

from src.utils import (
    get_currency_data,
    get_price_stock,
    information_for_each_card,
    top_five_transactions,
    welcome_function,
)


def home_page(data_time: Any) -> Any:
    """Функция для страницы «Главная» принимает на вход строку с датой
    и временем в формате YYYY-MM-DD HH:MM:SS."""
    try:
        response = {
            "greeting": welcome_function(),
            "cards": information_for_each_card(data_time),
            "top_transactions": top_five_transactions(data_time),
            "currency_rates": get_currency_data(),
            "stock_prices": get_price_stock(),
        }

        json.dumps(response)
        return response
    except Exception as e:
        print(f"Ошибка при обработке: {e}")
        return None


# print(home_page(pd.Timestamp("29-09-2018 00:00:00")))
