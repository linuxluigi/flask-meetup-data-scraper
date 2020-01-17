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
