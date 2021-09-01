_DATE_COLUMN_NAME = "dates"
_DATES_INNER_SEP = ":"
_DATES_OUTER_SEP = "|"


class TextFormat:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def confirm_input(input_value, valid_values):
    """ Takes input from the user until it is valid.

    Continues prompting the user for input until the input provided is equal to
    one of the valid values when converted to lower case.

    Args:
        input_value: the initial input provided from the user
        valid_values: a list of all strings that will be accepted.

    Returns:
        the input entered that matches one of the valid values

    Raises:
        EOFError: if the user force closes the input stream
        without providing valid input.
    """
    list_joiner = f"{TextFormat.END}, {TextFormat.GREEN}"
    str_list = (f"{TextFormat.GREEN}{list_joiner.join(valid_values)}"
                f"{TextFormat.END}")
    while input_value.lower() not in valid_values:
        print(f"{input_value} is not a valid option.")
        input_value = input(f"Please choose from {str_list}: ")
    return input_value


def process_dates_from_dict(data):
    """ Converts the dictionary representation of dates and quantity back to a
    string.

    Typically used to allow easy file writing of the pandas dataframe.

    Args:
        data: the dataframe containing the dictionary representation of dates
            and quantities. Will be the same dataframe and column the string
            representation is written to.
    """
    for index, row in data.iterrows():
        data.at[index, _DATE_COLUMN_NAME] = _DATES_OUTER_SEP.join(
            _DATES_INNER_SEP.join((key, val))
            for (key, val) in row[_DATE_COLUMN_NAME].items())


def process_dates_from_string(data):
    """ Converts string representation of quantity and dates to a dictionary
    contained inside the pandas dataframe.

    Args:
        data: the pandas dataframe containing the string representation in the
        'dates' column. Will be the same dataframe the dictionary is written
        to.
    """
    for index, row in data.iterrows():
        data.at[index, _DATE_COLUMN_NAME] = {
            item.split(_DATES_INNER_SEP)[0]: item.split(_DATES_INNER_SEP)[1]
            for item in row[_DATE_COLUMN_NAME].split(_DATES_OUTER_SEP)}


if __name__ == "__main__":
    confirm_input("Testing", ["one", "two"])
