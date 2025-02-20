#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import logging
from utils.sql_connection import Connector

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Логирование в файл
        logging.StreamHandler()         # Логирование в консоль
    ]
)

class SQLHandler:
    def __init__(self, db_name, file_path=None):
        self.db_name = db_name
        self.file_path = file_path
        self.connector = Connector(self.db_name)
        logging.info(f"Создан SQLHandler для базы данных '{self.db_name}'.")

    def connect_to_db(self):
        try:
            self.connector.connect()
            # logging.info("Успешное подключение к базе данных.")
        except Exception as e:
            logging.error(f"Ошибка подключения к базе данных: {e}")

    def close_connection(self):
        try:
            self.connector.close()
            # logging.info("Соединение с базой данных закрыто.")
        except Exception as e:
            logging.error(f"Ошибка при закрытии соединения: {e}")

    def import_data_from_csv(self):
        if self.file_path and os.path.exists(self.file_path):
            try:
                df = pd.read_csv(self.file_path)
                self.connector.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS water_usage (
                        country TEXT,
                        yearly_water_used REAL,
                        daily_water_used_per_capita REAL,
                        population INTEGER
                    )
                ''')
                df.to_sql('water_usage', self.connector.conn, if_exists='replace', index=False)
                logging.info("Данные успешно импортированы в SQLite базу данных.")
            except Exception as e:
                logging.error(f"Ошибка при импорте данных: {e}")
        else:
            logging.warning(f"Файл {self.file_path} не найден. Убедитесь, что путь указан правильно.")

    def execute_query(self, query):
        try:
            result = self.connector.execute_query(query)
            # logging.info(f"Запрос успешно выполнен: {query}")
            logging.info(f"Результат выполнения запроса: \n{result}")
            return result
        except Exception as e:
            logging.error(f"Ошибка выполнения запроса: {e}")
            return None

    def get_dataframe_from_query(self, query, columns):
        try:
            data = self.connector.execute_query(query)
            logging.info(f"Данные успешно получены из запроса: {query}")
            return pd.DataFrame(data, columns=columns)
        except Exception as e:
            logging.error(f"Ошибка при преобразовании данных в DataFrame: {e}")
            return pd.DataFrame()