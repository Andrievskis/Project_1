from typing import Any

import pandas as pd

from src.reports import reader_excel_file_, spending_by_category
from src.services import find_physical_transfers, reader_excel_file, simple_search
from src.views import home_page


def main() -> Any:
    """Функция для запуска всего проекта"""
    print("Веб-страницы (Главная): ")
    print(home_page(pd.Timestamp("29-09-2018 00:00:00")))

    print("Сервисы (Простой список; Поиск переводов физическим лицам): ")
    print(simple_search(input("Введите строку поиска: ").lower(), reader_excel_file))
    print(find_physical_transfers(reader_excel_file))

    print("Отчеты (Траты по категории): ")
    print(spending_by_category(reader_excel_file_, "ЖКХ", "20.05.2020"))


if __name__ == "__main__":
    main()
