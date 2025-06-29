import os
import csv


def open_read_csv(csv_file_name: str) -> list:
    """Open .csv file and return data as list of dictionaries."""
    if os.path.exists(csv_file_name):
        with open(csv_file_name, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
    else:
        raise FileNotFoundError('csv file not found!')
