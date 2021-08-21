import pandas as pd


def _confirm_input(input_value, valid_values):
    while input_value.lower() not in valid_values:
        print(f"{input_value} is not a valid option.")
        input_value = input(f"Selection from {', '.join(valid_values)}? ")
    return input_value


def _process_dates(data):
    outer_sep = "|"
    inner_sep = ":"
    column_name = "dates"
    for index, row in data.iterrows():
        data.at[index, column_name] = {
            item.split(inner_sep)[0]: item.split(inner_sep)[1]
            for item in row[column_name].split(outer_sep)}


def add_details(data):
    print("adding details not yet implemented")


def add_new_values(data):
    print("adding new data not yet implemented")


def start():
    decision = _confirm_input(
        input("Modifying drops or kills? "), ["drops", "kills"])
    # Set up the data
    data = pd.read_csv(f"{decision}.csv")
    _process_dates(data)

    decision = _confirm_input(
        input("Adding details or adding new values? "),
        ["details", "new values"])
    # Split into either section
    if decision == "details":
        add_details(data)
    else:
        add_new_values(data)


if __name__ == "__main__":
    start()
