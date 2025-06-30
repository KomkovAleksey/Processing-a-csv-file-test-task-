import os
import tempfile
import sys

import pytest

from main import (
    open_read_csv,
    parsed_string_from_terminal,
    convert_str_to_int,
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
    pass


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

    expected_resuls = [3.4, 4, -4, -3.4, 42, 0.5, 5]
    results = []
    for input_val, hass_error in test_cases:
        result = convert_str_to_int(input_val)
        if hass_error:
            captured = capsys.readouterr()
            assert captured.out == f'"{input_val}" is not a number\n'
        else:
            results.append(result)
    assert results == expected_resuls


def test_agrigate():
    pass
