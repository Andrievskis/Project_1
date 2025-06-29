import json
import logging
import re
from typing import Any

import pandas as pd

logger = logging.getLogger("services.log")
file_handler = logging.FileHandler("../logs/services.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

path_excel_file = "/Users/anastasiaandreeva/Project_1_banking_transaction_analysis_application/data/operations.xlsx"
reader_excel_file = (pd.read_excel(path_excel_file)).to_dict(orient="records")
# print(reader_excel_file)


def simple_search(search_str: str, data_list: list) -> Any:
    """Функция для простого поиска."""
    logger.info("Начало работы функции simple_search.")
    logger.warning("Тип вводных данных - str!")
    if not isinstance(search_str, str):
        logger.error("TypeError: Некорректный тип данных.")
        raise TypeError("Некорректный тип данных.")

    if search_str == "" or search_str == "nan" or not data_list:
        return []

    try:
        if not data_list:
            logger.error("Данные отсутствуют.")
            return []

        new_data_list = []
        for data in data_list:
            if isinstance(data.get("Категория"), str) and search_str.lower() in data["Категория"].lower():
                new_data_list.append(data)
            elif isinstance(data.get("Описание"), str) and search_str.lower() in data["Описание"].lower():
                new_data_list.append(data)

        json_result = json.dumps(new_data_list, indent=4, ensure_ascii=False)
        logger.info("Данные в виде JSON.")
        return json_result
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        return {e}
    finally:
        logger.info("Завершение работы функции simple_search.")


# print(simple_search(input('Введите строку поиска: ').lower(), reader_excel_file))


def find_physical_transfers(data_list: list) -> Any:
    """Функция поиска переводов физическим лицам."""
    logger.info("Начало работы функции find_physical_transfers.")
    try:
        if not data_list:
            logger.error("Данные отсутствуют.")
            return []

        name_pattern = r"[А-Яа-я]+\s[А-Яа-я]\."

        filtered_data = []
        for transaction in data_list:
            if transaction.get("Категория") == "Переводы" and re.search(name_pattern, transaction.get("Описание", "")):
                filtered_data.append(transaction)

        json_result = json.dumps(filtered_data, indent=4, ensure_ascii=False)

        logger.info("Данные в виде JSON.")
        return json_result
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        return {e}
    finally:
        logger.info("Завершение работы функции find_physical_transfers.")


# print(find_physical_transfers(reader_excel_file))
