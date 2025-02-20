#!/usr/bin/env python
# coding: utf-8

from sql_requests import SQLHandler
from visualization import Visualizer
from utils.clean_csv import CSVProcessor
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

def main():
    # Параметры
    input_csv = './data/water_use_by_country.csv'
    cleaned_csv = './data/water_use_by_country_cleaned.csv'
    db_name = 'water_usage.db'

    # Очистка CSV файла
    csv_processor = CSVProcessor(input_csv, cleaned_csv)
    csv_processor.clean_csv()

    # Импорт данных в базу данных
    sql_handler = SQLHandler(db_name, cleaned_csv)
    sql_handler.connect_to_db()
    sql_handler.import_data_from_csv()


    # Выполнение запросов
    # Вывод топ 5 стран с наибольшим расходом воды на душу населения
    query = '''
        SELECT
            country,
            "Yearly Water Used(m3, thousand of liters)",
            "Daily Water Used Per Capita(liters)",
            population
            FROM water_usage
            ORDER BY "Daily Water Used Per Capita(liters)" DESC
            LIMIT 5'''
    df = sql_handler.execute_query(query)


    # Вывод топ 5 стран с наименьшим расходом воды на душу населения
    query = '''
        SELECT
            country,
            "Yearly Water Used(m3, thousand of liters)",
            "Daily Water Used Per Capita(liters)",
            population
            FROM water_usage
            ORDER BY "Daily Water Used Per Capita(liters)"
            LIMIT 5'''
    df = sql_handler.execute_query(query)


    # Посмотрим данные по определённой стране
    query = '''
        SELECT
            country,
            "Yearly Water Used(m3, thousand of liters)",
            "Daily Water Used Per Capita(liters)",
            population
        FROM water_usage
        WHERE country = 'Belarus'
    '''
    df = sql_handler.execute_query(query)


    # Вывод стран с населением более 50 миллионов
    # и ежедневным использованием воды на душу населения выше 2000 литров
    query = '''
        SELECT
            country,
            `Yearly Water Used(m3, thousand of liters)`,
            `Daily Water Used Per Capita(liters)`,
            population
        FROM water_usage
        WHERE population > 50000000
        AND `Daily Water Used Per Capita(liters)` > 2000
        ORDER BY population DESC
    '''
    df = sql_handler.execute_query(query)


    # Вывод стран, где годовое использование воды превышает среднее значение
    query = '''
        SELECT
            country,
            `Yearly Water Used(m3, thousand of liters)`,
            `Daily Water Used Per Capita(liters)`,
            population
        FROM water_usage
        WHERE `Yearly Water Used(m3, thousand of liters)` > (
            SELECT AVG(`Yearly Water Used(m3, thousand of liters)`)
            FROM water_usage
        )
        ORDER BY `Yearly Water Used(m3, thousand of liters)` DESC
    '''
    df = sql_handler.execute_query(query)



    query = '''SELECT * FROM water_usage'''
    columns = ['Country', 'yearly_water_used(m3)', 'daily_water_used_per_capita(l)', 'Population']
    df = sql_handler.get_dataframe_from_query(query, columns)

    # Построение графиков
    visualizer = Visualizer()
    visualizer.plot_top_10_daily_water_usage(df)
    visualizer.plot_top_10_yearly_water_usage(df)
    visualizer.plot_boxplot_daily_water_usage(df)
    visualizer.plot_scatter_population_vs_water_usage(df)


    # Закрытие соединения
    sql_handler.close_connection()

if __name__ == '__main__':
    main()