import os
import csv
import argparse
import sys
import operator

from tabulate import tabulate


def open_read_csv(csv_file_name: str) -> list:
    """Open .csv file and return data as list of dictionaries."""
    if os.path.exists(csv_file_name):
        with open(csv_file_name, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
    raise FileNotFoundError('csv file not found!')


def parsed_string_from_terminal(parsed_string: str) -> tuple:
    """Parses the string into (column, operator, value)."""
    operators = {
        '<': operator.lt,
        '>': operator.gt,
        '=': operator.eq,
    }
    for operator_str in operators:
        if operator_str in parsed_string:
            column, value = parsed_string.split(operator_str)
            return column, operator_str, value, operators[operator_str]
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


def agrigate(data, column: str, operator_str: str, value: str) -> list:
    """Perform aggregation (min, max, avg) on numeric column data."""
    if operator_str == '=':
        values_from_data = [
            item[column] for item in data if column in item
        ]
        values_from_data_int = []
        for num in values_from_data:
            a = convert_str_to_int(num)
            values_from_data_int.append(a)
        if value == 'min':
            return [dict.fromkeys([value], min(values_from_data_int))]

        elif value == 'max':
            return [dict.fromkeys([value], max(values_from_data_int))]

        elif value == 'avg':
            return [
                dict.fromkeys(
                    [value],
                    sum(values_from_data_int) / len(values_from_data_int)
                )]
        else:
            raise ValueError(f'{value} must be a func(min, max, avg)')
    else:
        raise ValueError(f'{operator_str} must be a "="')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Processing a csv file.',
        )
    parser.add_argument(
        '--file',
        required=True,
        help='Enter the name of the csv file.',
    )
    parser.add_argument(
        '--where',
        help='Filtering condition in the format "column=value"',
    )
    parser.add_argument(
        '--aggregate',
        help='Aggregation in the format "function=column"',
    )

    args = parser.parse_args()

    try:
        data = open_read_csv(args.file)
    except Exception as e:
        print(f'File Read Error: {e}', file=sys.stderr)
        sys.exit(1)

    if args.where:
        try:
            column, operator_str, value, operator_func = (
                parsed_string_from_terminal(args.where)
            )
            value = convert_str_to_int(value)
            result = [
                row for row in data
                if operator_func(convert_str_to_int(row.get(column, 0)), value)
            ]
            print(tabulate(
                result,
                headers='keys',
                tablefmt='psql',
            ))
        except Exception as e:
            print(f'Error in the filtering condition: {e}', file=sys.stderr)
            sys.exit(1)

    elif args.aggregate:
        try:
            column, operator_str, value, operator_func = (
                parsed_string_from_terminal(args.aggregate)
            )
            result = agrigate(data, column, operator_str, value)
            print(tabulate(
                result,
                headers='keys',
                tablefmt='psql',
            ))

        except Exception as e:
            print(f'Error in the aggregation condition: {e}', file=sys.stderr)
            sys.exit(1)

    else:
        print(tabulate(
            data,
            headers='keys',
            tablefmt='psql',
        ))
