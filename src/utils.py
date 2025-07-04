import json
import logging
import os
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY_CURRENCY = os.getenv("API_KEY_CURRENCY")
API_KEY_SP_500 = os.getenv("API_KEY_SP_500")

logger = logging.getLogger("utils.log")
file_handler = logging.FileHandler("../logs/utils.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def read_excel(path_excel: str) -> Any:
    """Функция для считывания финансовых операций из Excel."""
    logger.info("Начало работы функции read_excel.")
    logger.info("Чтение данных из operations.xlsx")
    try:
        reader_excel_file = (pd.read_excel(path_excel)).to_dict(orient="records")
        logger.info("Данные о финансовых операция в виде списка словарей.")
        return reader_excel_file
    except (FileNotFoundError, Exception) as e:
        logger.error(f"Произошла ошибка в функции read_excel: {e}")
        return f"Произошла ошибка: {e}"
    finally:
        logger.info("Завершение работы функции read_excel.")


path_excel_file = "/Users/anastasiaandreeva/Project_1_banking_transaction_analysis_application/data/operations.xlsx"
# print(read_excel(path_excel_file))


def welcome_function() -> str | Any:
    """Функция приветствия."""
    logger.info("Начало работы функции greeting.")
    try:
        current_date_time = datetime.now()
        hour = current_date_time.hour

        if 0 <= hour < 6 or 22 <= hour <= 23:
            return "Доброй ночи"
        elif 17 <= hour <= 22:
            return "Добрый вечер"
        elif 7 <= hour <= 11:
            return "Доброе утро"
        else:
            return "Добрый день"
    except Exception as e:
        logger.error(f"Произошла ошибка в функции welcome_function: {e}")
        return {e}
    finally:
        logger.info("Завершение работы функции welcome_function.")


# print(welcome_function())


def information_for_each_card(data_time: pd.Timestamp) -> Any:
    """Функция информации по каждой карте."""
    logger.info("Начало работы функции information_for_each_card.")
    try:
        logger.info("Чтение данных из operations.xlsx")
        df = pd.read_excel(path_excel_file)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
        start_date = data_time.replace(day=1)
        end_date = data_time

        df_filtered = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)].copy()

        df_filtered["кэшбек"] = df_filtered["Сумма операции с округлением"] * 0.01

        grouped = (
            df_filtered.groupby("Номер карты")
            .agg(total_spent=("Сумма операции с округлением", "sum"), cashback=("кэшбек", "sum"))
            .reset_index()
        )

        grouped["last_digits"] = grouped["Номер карты"].astype(str).str[-4:]

        result_df = grouped.sort_values(by="total_spent", ascending=False)

        result = result_df[["last_digits", "total_spent", "cashback"]].to_dict("records")

        for item in result:
            item["total_spent"] = round(item["total_spent"], 2)
            item["cashback"] = round(item["cashback"], 2)

        logger.info("Данные в виде списка словарей.")
        return result
    except Exception as e:
        logger.error(f"Произошла ошибка в функции information_for_each_card: {e}")
        return f"{e}"
    finally:
        logger.info("Завершение работы функции information_for_each_card.")


# print(information_for_each_card(pd.to_datetime('29-09-2018 00:00:00', dayfirst=True)))


def top_five_transactions(data_time: pd.Timestamp) -> Any:
    """Топ-5 транзакций по сумме платежа."""
    logger.info("Начало работы функции top_five_transactions.")
    try:
        logger.info("Чтение данных из operations.xlsx")
        df = pd.read_excel(path_excel_file)

        df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S", dayfirst=True)

        start_date = data_time.replace(day=1)
        end_date = data_time

        filtered_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)].copy()

        top_transactions = filtered_df.sort_values(by="Сумма операции с округлением", ascending=False).head(5)

        result = top_transactions.apply(
            lambda row: {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": round(row["Сумма операции с округлением"], 2),
                "category": row["Категория"],
                "description": row["Описание"],
            },
            axis=1,
        ).tolist()

        logger.info("Данные в виде списка словарей.")
        return result
    except Exception as e:
        logger.error(f"Произошла ошибка в функции top_five_transactions: {e}")
        return {e}
    finally:
        logger.info("Завершение работы функции top_five_transactions.")


# print(top_five_transactions(pd.to_datetime('29.09.2020', dayfirst=True)))


def get_currency_data() -> Any:
    """Функция для получения курсов валют."""
    logger.info("Начало работы функции get_currency_data.")
    try:
        result = []
        path_json_file = (
            "/Users/anastasiaandreeva/Project_1_banking_transaction_analysis_application/user_settings.json"
        )
        logger.info("Чтение данных из user_settings.json.")
        with open(path_json_file, "r", encoding="utf=8") as f:
            data = (json.load(f)).get("user_currencies")
            for user_currencies in data:
                url = f"https://v6.exchangerate-api.com/v6/{API_KEY_CURRENCY}/latest/{user_currencies}"
                response = requests.get(url)
                if response.status_code == 200:
                    response.json()
                    result.append(
                        {"currency": user_currencies, "rate": round(response.json()["conversion_rates"]["RUB"], 2)}
                    )
        logger.info("Данные в виде списка словарей.")
        return result
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        return f"Произошла ошибка: {e}"
    finally:
        logger.info("Завершение работы функции get_currency_data.")


# print(get_currency_data())


def get_price_stock() -> Any:
    """Функция для получения стоимости акций из S&P500."""
    logger.info("Начало работы функции get_price_stock.")
    try:
        result = []
        path_json_file = (
            "/Users/anastasiaandreeva/Project_1_banking_transaction_analysis_application/user_settings.json"
        )
        logger.info("Чтение данных из user_settings.json.")
        with open(path_json_file, "r", encoding="utf=8") as f:
            data = (json.load(f)).get("user_stocks")
            for user_stocks in data:
                url = (
                    f"https://www.alphavantage."
                    f"co/query?function=GLOBAL_QUOTE&symbol={user_stocks}&apikey={API_KEY_SP_500}"
                )
                response = requests.get(url)
                if response.status_code == 200:
                    response.json()
                    result.append(
                        {"stock": user_stocks, "price": round(float(response.json()["Global Quote"]["05. price"]), 2)}
                    )
        logger.info("Данные в виде списка словарей.")
        return result
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        return f"Произошла ошибка: {e}"
    finally:
        logger.info("Завершение работы функции get_price_stock.")


# print(get_price_stock())
