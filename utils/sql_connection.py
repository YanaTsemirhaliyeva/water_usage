import sqlite3
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

class Connector:
    def __init__(self, db_name='water_usage.db'):
        # Инициализация соединения с базой данных
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        logging.info(f"Инициализирован Connector для базы данных '{self.db_name}'.")

    def connect(self):
        # Подключение к базе данных
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logging.info(f"Успешное подключение к базе данных '{self.db_name}'.")
        except Exception as e:
            logging.error(f"Ошибка подключения к базе данных: {e}")

    def execute_query(self, query):
        # Выполнение запроса и возврат результата
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            logging.info(f"Запрос выполнен: {query}")
            return result
        except Exception as e:
            logging.error(f"Ошибка выполнения запроса: {e}")
            return None

    def close(self):
        # Закрытие соединения с базой данных
        try:
            if self.conn:
                self.conn.commit()
                self.conn.close()
                logging.info("Соединение с базой данных закрыто.")
        except Exception as e:
            logging.error(f"Ошибка при закрытии соединения: {e}")