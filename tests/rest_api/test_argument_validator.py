from typing import List

import pytest

from meetup_search.rest_api.argument_validator import (
    date_validator,
    positive_int_validator,
    string_list_validator,
)


def test_string_list_validator():
    # check for valid values
    valid_values: List = [
        "name",
    ]

    for value in valid_values:
        assert string_list_validator(value=value) == value

    # check for invalid values
    invalid_values: List = [[""], 0, 0.0, True, False, "", {}]

    for value in invalid_values:
        with pytest.raises(ValueError):
            string_list_validator(value=value)


def test_positive_int_validator():
    # check for valid filter
    valid_values: List = [
        0,
        5,
        25,
    ]

    for value in valid_values:
        assert positive_int_validator(value=value) == value

    # check for invalid values
    invalid_values: List = [[""], -1, "one"]

    for value in invalid_values:
        with pytest.raises(ValueError):
            positive_int_validator(value=value)


def test_date_validator():
    # check for valid filter
    valid_values: List = [
        "2012-12-12",
    ]

    for value in valid_values:
        assert isinstance(date_validator(value=value), str)

    # check for invalid values
    invalid_values: List = ["Bernd ist ein Brot"]

    for value in invalid_values:
        with pytest.raises(ValueError):
            date_validator(value=value)
