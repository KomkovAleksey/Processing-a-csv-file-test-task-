import os
import csv


def open_read_csv(csv_file_name: str) -> list:
    """Open .csv file and return data as list of dictionaries."""
    if os.path.exists(csv_file_name):
        with open(csv_file_name, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
    raise FileNotFoundError('csv file not found!')


def parsed_string_from_terminal(parsed_string: str) -> tuple:
    """Parses the string into (column, operator, value)."""
    operators = ['=', '<', '>',]
    for operator_str in operators:
        if operator_str in parsed_string:
            column, value = parsed_string.split(operator_str)
            return column, operator_str, value
    raise ValueError(
        f'Invalid condition: {parsed_string} must contain "=", "<" or">"'
    )


def convert_str_to_int(value: str):
    """
    Converts a string to a number (int/float),
    if a string is made up of numbers,
    otherwise returns a string.
    """
    try:
        value = float(value)
        if value.is_integer():
            return int(value)
        return value
    except ValueError:
        print(f'"{value}" is not a number')

        return value
