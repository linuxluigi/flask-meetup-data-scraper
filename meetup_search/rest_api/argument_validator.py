from datetime import date, datetime


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


def date_validator(value: str) -> str:
    """
    Validate if string is a valid date

    Arguments:
        value {str} -- value to validate

    Returns:
        str -- validate date as string
    """

    try:
        return str(
            datetime.fromisoformat(value).date()
        )
    except TypeError:
        raise ValueError("Can't convert value to date!")
