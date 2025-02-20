#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import os
import seaborn as sns
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Логирование в файл
        logging.StreamHandler()         # Логирование в консоль
    ]
)

class Visualizer:
    def __init__(self, output_dir='public'):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logging.info(f"Создана директория для сохранения графиков: {self.output_dir}")
        sns.set(style="whitegrid")
        logging.info("Инициализирован Visualizer.")

    def plot_top_10_daily_water_usage(self, df):
        try:
            top_countries = df.sort_values('daily_water_used_per_capita(l)', ascending=False).head(10)
            plt.figure(figsize=(14, 8))
            sns.barplot(x='daily_water_used_per_capita(l)', y='Country', data=top_countries, palette='viridis', hue='Country')
            plt.title('Топ-10 стран по суточному потреблению воды на душу населения')
            plt.xlabel('Суточное потребление воды (литры)')
            plt.ylabel('Страна')
            plt.savefig(f'{self.output_dir}/top_10_water_usage_daily.png', format='png', dpi=300, bbox_inches='tight')
            plt.show()
            logging.info("График 'Топ-10 по суточному потреблению воды' успешно сохранён.")
        except Exception as e:
            logging.error(f"Ошибка при построении графика: {e}")

    def plot_top_10_yearly_water_usage(self, df):
        try:
            top_countries = df.sort_values('yearly_water_used(m3)', ascending=False).head(10)
            plt.figure(figsize=(14, 8))
            sns.barplot(x='yearly_water_used(m3)', y='Country', data=top_countries, palette='viridis', hue='Country')
            plt.title('Топ-10 стран по годовому потреблению воды')
            plt.xlabel('Годовое потребление воды (м³)')
            plt.ylabel('Страна')
            plt.savefig(f'{self.output_dir}/top_10_water_usage_yearly.png', format='png', dpi=300, bbox_inches='tight')
            plt.show()
            logging.info("График 'Топ-10 по годовому потреблению воды' успешно сохранён.")
        except Exception as e:
            logging.error(f"Ошибка при построении графика: {e}")

    def plot_boxplot_daily_water_usage(self, df):
        try:
            plt.figure(figsize=(10, 6))
            sns.boxplot(y='daily_water_used_per_capita(l)', data=df)
            plt.title('Ящик с усами для суточного потребления воды на душу населения')
            plt.ylabel('Суточное потребление воды (литры)')
            plt.grid(axis='y', alpha=0.75)
            plt.savefig(f'{self.output_dir}/boxplot_for_daily_water_consumption.png', format='png', dpi=300, bbox_inches='tight')
            plt.show()
        except Exception as e:
            logging.error(f"Ошибка при построении графика: {e}")

    def plot_scatter_population_vs_water_usage(self, df):
        try:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x='Population', y='daily_water_used_per_capita(l)', data=df)
            plt.title('Зависимость суточного потребления воды от населения')
            plt.xlabel('Население')
            plt.ylabel('Суточное потребление воды (литры)')
            plt.xscale('log')  # Логарифмическая шкала для населения
            plt.grid()
            plt.savefig(f'{self.output_dir}/dependence_of_daily_water_consumption.png', format='png', dpi=300, bbox_inches='tight')
            plt.show()
        except Exception as e:
            logging.error(f"Ошибка при построении графика: {e}")