import csv
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

class CSVProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def clean_csv(self):
        try:
            with open(self.input_file, 'r') as infile, open(self.output_file, 'w', newline='') as outfile:
                reader = csv.reader(infile)
                writer = csv.writer(outfile)

                headers = next(reader)  # Чтение заголовков
                writer.writerow(headers)  # Запись заголовков

                for row in reader:
                    row[1] = row[1].replace(',', '')  # Удаление запятых из Yearly Water Used
                    row[2] = row[2].replace(',', '')  # Удаление запятых из Daily Water Used Per Capita
                    row[3] = row[3].replace(',', '')  # Удаление запятых из Population
                    writer.writerow(row)

            logging.info(f"CSV файл успешно очищен и сохранён в '{self.output_file}'.")
        except Exception as e:
            logging.error(f"Ошибка при обработке CSV файла: {e}")