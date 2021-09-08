from util import TextFormat
from util import confirm_input
from util import make_filename
from util import read_data_from_csv
from util import write_data_to_csv

_TESTING = True


def _scroll(data, data_name):
    data = data.sort_values(data_name)
    stop_words = ["stop", "quit", "q"]
    for index, row in data.iterrows():
        user_in = input(f"{TextFormat.BLUE}{row[data_name]}{TextFormat.END} ")
        if user_in in stop_words:
            return

        # TODO: allow starting the merging process directly from here by the
        # user typing something to choose the first one

        # TODO: continuing from above allow the user to scroll for the second
        # choice (or from starting the list below) using arrow keys or vim
        # commands)


def _calc_index(df, matching_value, col_name):
    """
    Returns -1 if such a row is not found, otherwise returns the appriorate
        index.
    """
    try:
        return df.index[df[col_name] == matching_value].item()
    except ValueError:
        raise ValueError()


def _fetch_row_from_dataframe_given_name(df, name, col_name):
    """ Returns a row from the dataframe that matches the specific name given.
    """
    try:
        return df.iloc[_calc_index(df, name, col_name)]
    except ValueError:
        return None


def _merge_dates_dict(dates1, dates2):
    for date in dates2:
        if date in dates1:
            dates1[date] += dates2[date]
        else:
            dates1[date] = dates2[date]


def _merge_items(df, col_name):
    # NOTE: this keeps all the data from the first item selected not the second
    # Making the deliberate choice to keep this CASE SENSITIVE to allow merging
    # when the only difference is case
    option_list = df[col_name].tolist()
    item1_name = confirm_input(
        input("What is the first item you would like to merge? "),
        option_list + ["cancel"],
        case_sensitive=True)

    if item1_name == "cancel":
        return
    option_list.remove(item1_name)

    item2_name = confirm_input(
        input("What is the second item you would like to merge? "),
        option_list + ["cancel"],
        case_sensitive=True)
    if item2_name == "cancel":
        return

    item1 = _fetch_row_from_dataframe_given_name(df, item1_name, col_name)
    item2 = _fetch_row_from_dataframe_given_name(df, item2_name, col_name)

    if item1 is None or item2 is None:
        print(f"One of the items {TextFormat.RED}does not exist"
              f"{TextFormat.END}. Please select a different option or"
              " try again.")
        return

    updated_name = input(f"What is the name of the merged item (current names"
                         f" are {TextFormat.GREEN}{item1_name}{TextFormat.END}"
                         f" and {TextFormat.GREEN}{item2_name}{TextFormat.END}"
                         "? ")
    # TODO: if there are any differences between the remaining columns question
    # those

    _merge_dates_dict(item1["dates"], item2["dates"])
    df = df.drop(index=_calc_index(df, item2_name, col_name))
    df.at[_calc_index(df, item1_name, col_name), col_name] = updated_name

    write_data_to_csv(make_filename(_TESTING, f"{col_name}s"), df)


def _sort_and_print(data, data_name):
    print()
    data = data.sort_values(data_name)
    for index, row in data.iterrows():
        print(row[data_name])
    print()


def combine_items():
    data_name = confirm_input(
        input(f"Combining {TextFormat.GREEN}kills{TextFormat.END} or "
              f"{TextFormat.GREEN}drops{TextFormat.END}? "),
        ["kills", "drops"])
    data = read_data_from_csv(make_filename(_TESTING, data_name))
    data_name = data_name[:-1]

    _sort_and_print(data, data_name)

    while True:
        user_input = confirm_input(
            input(f"What would you like to do now ({TextFormat.GREEN}merge"
                  f"{TextFormat.END}, {TextFormat.GREEN}scroll{TextFormat.END}"
                  f", or {TextFormat.GREEN}quit{TextFormat.END})? "),
            ["merge", "scroll", "quit"])
        if user_input == "quit":
            break
        if user_input == "scroll":
            _scroll(data, data_name)
        if user_input == "merge":
            _merge_items(data, data_name)
        break


def start():
    opt = confirm_input(
        input(f"Are you wanting to {TextFormat.GREEN} combine"
              f"{TextFormat.END} or ... ? "),
        ["combine"])
    opt = "combine"
    if opt == "combine":
        combine_items()


if __name__ == "__main__":
    if _TESTING:
        print(f"{TextFormat.PURPLE}In Testing Mode!!!!!{TextFormat.END}")
    start()
