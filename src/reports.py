import json
import logging
from datetime import date, datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Union

import pandas as pd

logger = logging.getLogger("reports.log")
file_handler = logging.FileHandler("../logs/reports.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

path_excel_file = "/Users/anastasiaandreeva/Project_1_banking_transaction_analysis_application/data/operations.xlsx"
reader_excel_file_ = pd.read_excel(path_excel_file)


def report_saver(file_name: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Декоратор для сохранения результатов отчетов в файл."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            # Преобразуем даты в строки
            if isinstance(result, list):
                for item in result:
                    for key, value in item.items():
                        if isinstance(value, datetime):
                            item[key] = value.strftime("%Y-%m-%d %H:%M:%S")

            if file_name is None:
                default_file_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                file_path = default_file_name
            else:
                file_path = file_name

            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)
                logger.info(f"Отчет успешно сохранен в файл: {file_path}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении отчета: {str(e)}")

            return result

        return wrapper

    return decorator


@report_saver("custom_report.json")
def spending_by_category(
    data_list: Union[pd.DataFrame, str], category: str, date: Optional[Union[str, datetime, date]] = None
) -> Union[pd.DataFrame, List[Dict]]:
    """Траты по категории."""
    logger.info("Начало работы функции spending_by_category.")

    try:
        if date is None:
            date = datetime.now()
        elif isinstance(date, str):
            date = pd.to_datetime(date, dayfirst=True)
        elif isinstance(date, datetime):
            date = date
        elif isinstance(date, datetime):
            date = datetime.combine(date, datetime.min.time())

        if isinstance(data_list, str):
            df = pd.read_excel(data_list)
        else:
            df = data_list

        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

        filtered_transactions = df[df["Категория"] == category]

        start_date = date - timedelta(days=90)
        end_date = date

        recent_transactions = filtered_transactions[
            (filtered_transactions["Дата операции"] >= start_date)
            & (filtered_transactions["Дата операции"] <= end_date)
        ]

        logger.info("Траты по заданной категории за последние 3 месяца от переданной даты.")
        return recent_transactions.to_dict("records")

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        return [{"error": str(e)}]

    finally:
        logger.info("Завершение работы функции spending_by_category.")


print(spending_by_category(reader_excel_file_, "ЖКХ", "20.05.2020"))
