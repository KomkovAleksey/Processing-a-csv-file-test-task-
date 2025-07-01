import os
import tempfile
import operator

import pytest

from main import (
    open_read_csv,
    parsed_string_from_terminal,
    convert_str_to_int_or_float,
    agrigate,
)


def test_open_read_csv_file():
    """
    Test for reading a temporary CSV file
    with test_open_read_csv_file func.
    """
    temporary_csv_file = (
        'name,year,rating'
        '\nDrunken Master,1978,7.5'
        '\nProject A,1983,7.3'
    )
    with tempfile.NamedTemporaryFile(
        mode='w+',
        delete=False,
        suffix='.csv'
    ) as tmp:
        tmp.write(temporary_csv_file)
        tmp_path = tmp.name

    result = open_read_csv(tmp_path)
    os.unlink(tmp_path)

    assert result == [
        {'name': 'Drunken Master',
         'year': '1978',
         'rating': '7.5',
         },
        {'name': 'Project A',
         'year': '1983',
         'rating': '7.3',
         },
    ]


def test_open_read_csv_file_not_found():
    """Test for handling missing .csv files."""
    with pytest.raises(FileNotFoundError) as excinfo:
        open_read_csv('non_existent_file.csv')
    assert 'csv file not found!' in str(excinfo.value)


def test_parsed_string_from_terminal():
    """Test parsed_string_from_terminal func."""
    test_cases = [
        ('age=25', False),
        ('salary<50000', False),
        ('height>180', False),
        ('age = 25', False),
        ('name = John Doe', False),
        ('age>=30', False),
        ('score<=100', False),
        ('name=', False),
        ('=value', False),
        ('user@name=john.doe', False),
        ('price>$100', False),
        ('age25', True),
        ('age!25', True),
        ('', True),
        ('no_operator', True),
    ]
    expected_resuls = [
        ('age', '=', '25', operator.eq),
        ('salary', '<', '50000', operator.lt),
        ('height', '>', '180', operator.gt),
        ('age', '=', '25', operator.eq),
        ('name', '=', 'John Doe', operator.eq),
        ('age', '>', '=30', operator.gt),
        ('score', '<', '=100', operator.lt),
        ('name', '=', '', operator.eq),
        ('', '=', 'value', operator.eq),
        ('user@name', '=', 'john.doe',  operator.eq),
        ('price', '>', '$100', operator.gt),

    ]
    results = []
    for input_val, hass_error in test_cases:
        if hass_error:
            with pytest.raises(ValueError) as exc_info:
                parsed_string_from_terminal(input_val)
            assert 'must contain "=", "<" or">"' in str(exc_info.value)
        else:
            result = parsed_string_from_terminal(input_val)
            results.append(result)

    assert results == expected_resuls


def test_convert_str_to_int(capsys):
    """Test  convert_str_to_int func."""
    test_cases = [
        ('3.4', False),
        ('4', False),
        ('-4', False),
        ('-3.4', False),
        ('42.0', False),
        ('.5', False),
        ('5.', False),
        ('num', True),
        ('', True),
        ('  ',  True),
        ('3.4num', True),
        ('4num', True),
        ('12.34.56', True),
    ]

    expected_results = [3.4, 4, -4, -3.4, 42, 0.5, 5]
    results = []
    for input_val, hass_error in test_cases:
        result = convert_str_to_int_or_float(input_val)
        if hass_error:
            captured = capsys.readouterr()
            assert captured.out == f'"{input_val}" is not a number\n'
        else:
            results.append(result)
    assert results == expected_results


def test_agrigate():
    """Test agrigate func."""
    test_data = [
        {'rating': '7.7'},
        {'rating': '6.7'},
        {'rating': '7.8'},
        {'rating': '8.2'},
        {'rating': '7.6'},
        {'rating': '8.0'},
        {'rating': '7.6'},
        {'rating': '7.6'},
        {'rating': '6.2'},
        {'rating': '5.3'},

    ]

    test_cases = [
        (test_data, 'rating', '=', 'min', False),
        (test_data, 'rating', '=', 'max', False),
        (test_data, 'rating', '=', 'avg', False),

        (test_data, 'rating', '<', 'max', True),
        (test_data, 'rating', '=', 'sim', True),
    ]

    expected_resuls = [[{'min': 5.3}], [{'max': 8.2}], [{'avg': 7.3}]]
    results = []
    for data, column, operator_str, value, hass_error in test_cases:
        if hass_error:
            with pytest.raises(ValueError) as exc_info:
                agrigate(data, column, operator_str, value)
            if operator_str != '=':
                assert 'must be a "="' in str(exc_info.value)
            if value not in ['min', 'max', 'avg']:
                assert 'must be a func' in str(exc_info.value)
        else:
            result = agrigate(data, column, operator_str, value)
            results.append(result)

    assert results == expected_resuls
