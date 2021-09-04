import pandas as pd

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


def _process_dates_from_string(data):
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


def read_data_from_csv(testing, data_type):
    """ Reads in the csv of the given data type (drops or kills) and returns it
    in the form of a pandas dataframe.

    Args:
        testing: whether the program is in testing mode
        data_type: the type of the data being read. Can either be drops
            or kills.

    Returns:
        The dataframe created from this csv.

    Raises:
        AttributeError: if the provided data_type is not either drops or kills.
    """
    if data_type != "drops" and data_type != "kills":
        raise AttributeError(f"{data_type} is not a valid data type")

    filename = (f"test_data/{data_type}.csv" if testing
                else f"{data_type}.csv")
    data = pd.read_csv(filename)
    _process_dates_from_string(data)

    return data


if __name__ == "__main__":
    confirm_input("Testing", ["one", "two"])
