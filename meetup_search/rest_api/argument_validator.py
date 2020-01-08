from typing import List


def string_list_validator(value: str) -> str:
    """
    Validate if value is a str

    Arguments:
        value {str} -- value to validate

    Raises:
        ValueError: value is not a type of str
        ValueError: Value can't be a empty string

    Returns:
        str -- unchanged input value
    """

    # raise when list element (value) is not an string
    if not isinstance(value, str):
        raise ValueError("All values has to be an string! List[str]")

    if value == "":
        raise ValueError("Value can't be a empty string! List[str]")

    return value


def filter_validator(value: dict) -> dict:
    """
    Validate filter search query

    Arguments:
        value {dict} -- Filter dict

    Raises:
        ValueError: Value is not an dict
        ValueError: Dict has no content

    Returns:
        dict -- unchanged input value
    """

    # todo check for possible filters!

    # raise when value is not an dict
    if not isinstance(value, dict):
        raise ValueError("Filters has to be a dict!")

    # raise when dict has no content
    if len(value) == 0:
        raise ValueError("Dict has no content")

    return value


def positive_int_validator(value: int) -> int:
    """
    Validate for positive int

    Arguments:
        value {int} -- int number

    Raises:
        ValueError: Value is an str that can not convert to an int
        ValueError: Value has to be an int
        ValueError: Value has to be equal or greater than 0

    Returns:
        int -- unchanged input value
    """

    # raise when value is not an int
    if isinstance(value, str):
        try:
            value = int(value)
        except ValueError:
            raise ValueError("Value has to be an int!")

    # raise when value is not an int
    if not isinstance(value, int):
        raise ValueError("Value has to be an int!")

    # raise when value is smaller than 0
    if value < 0:
        raise ValueError("Value has to be equal or greater than 0!")

    return value


def sort_validator(value: dict) -> dict:
    """
    Validate 
    
    Arguments:
        value {dict} -- Sort dict
    
    Raises:
        ValueError: Value is not an dict
        ValueError: Value is not an empty dict
        ValueError: Value Key  is an empty string
        ValueError: Each sort element needs to have order & more
        ValueError: Invalid sort order option
        ValueError: Invalid sort mode option
    
    Returns:
        dict -- unchanged input value
    """

    example: str = "List[{'lines' : {'order' : 'asc', 'mode' : 'avg'}}]"

    # raise when value is is not an dict
    if not isinstance(value, dict):
        raise ValueError("Search element has to be a dict like {}".format(example))

    # raise when value is is an empty dict
    if value == {}:
        raise ValueError("Search element can't be empty!")

    for key in value:

        # raise when key is an empty string
        if key == "":
            raise ValueError(
                "Search element key can't be an empty string! {}".format(example)
            )

        # raise when value has no element of order or mode
        if not "order" in value[key] or not "mode" in value[key]:
            raise ValueError(
                "Each Element need to have a dict with order & more like: {}".format(
                    example
                )
            )

        # raise by invalid sort order
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html#_sort_order
        sort_order_options: List[str] = ["asc", "desc"]
        if not value[key]["order"] in sort_order_options:
            raise ValueError("Invalid sort order option: {}".format(sort_order_options))

        # raise by invalid sort option
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html#_sort_mode_option
        sort_mode_options: List[str] = ["min", "max", "sum", "avg", "median"]
        if not value[key]["mode"] in sort_mode_options:
            raise ValueError("Invalid sort mode option: {}".format(sort_mode_options))

    return value
