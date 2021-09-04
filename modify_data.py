from util import TextFormat
from util import confirm_input
from util import read_data_from_csv

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


def _merge(data, data_name):
    pass
    # Allow the user to enter the name of item 1

    # Allow the user to enter the name of second item

    # Allow the user to select the name to keep

    # Do the merge


def _sort_and_print(data, data_name):
    print()
    data = data.sort_values(data_name)
    for index, row in data.iterrows():
        print(row[data_name])
    print()


def combine():
    """
    data_name = confirm_input(
        input(f"Combining {TextFormat.GREEN}kills{TextFormat.END} or "
              f"{TextFormat.GREEN}drops{TextFormat.END}? "),
        ["kills", "drops"])
    """
    data_name = "drops"
    data = read_data_from_csv(_TESTING, data_name)
    data_name = data_name[:-1]

    _sort_and_print(data, data_name)

    while True:
        """
        user_input = confirm_input(
            input(f"What would you like to do now ({TextFormat.GREEN}merge"
                  f"{TextFormat.END}, {TextFormat.GREEN}scroll{TextFormat.END}"
                  f", or {TextFormat.GREEN}quit{TextFormat.END})? "),
            ["merge", "scroll", "quit"])
        """
        user_input = "merge"
        if user_input == "quit":
            break
        if user_input == "scroll":
            _scroll(data, data_name)
        if user_input == "merge":
            _merge(data, data_name)
        break


    # Update the csv


def start():
    """
    opt = confirm_input(
        input(f"Are you wanting to {TextFormat.GREEN} combine"
              f"{TextFormat.END} or ... ? "),
        ["combine"])
    """
    opt = "combine"
    if opt == "combine":
        combine()


if __name__ == "__main__":
    if _TESTING:
        print(f"{TextFormat.PURPLE}In Testing Mode!!!!!{TextFormat.END}")
    start()
