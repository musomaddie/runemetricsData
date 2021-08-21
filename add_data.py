import pandas as pd
DATE_COLUMN_NAME = "dates"


def _confirm_input(input_value, valid_values):
    while input_value.lower() not in valid_values:
        print(f"{input_value} is not a valid option.")
        input_value = input(f"Selection from {', '.join(valid_values)}? ")
    return input_value


def _process_dates(data):
    outer_sep = "|"
    inner_sep = ":"
    for index, row in data.iterrows():
        data.at[index, DATE_COLUMN_NAME] = {
            item.split(inner_sep)[0]: item.split(inner_sep)[1]
            for item in row[DATE_COLUMN_NAME].split(outer_sep)}


def _unprocess_dates(data):
    outer_sep = "|"
    inner_sep = ":"
    for index, row in data.iterrows():
        data.at[index, DATE_COLUMN_NAME] = outer_sep.join(
            inner_sep.join((key, val))
            for (key, val) in row[DATE_COLUMN_NAME].items())


def _add_value(data, date, item, quantity, item_type):
    if item in data[item_type].values:
        existing_dict = data.loc[
            data.index[data[item_type] == item]][DATE_COLUMN_NAME][0]
        existing_dict[date] = quantity
    else:
        # Create new series
        series = pd.Series(
            data={
                item_type: item,
                DATE_COLUMN_NAME: {date: quantity}},
            index=[item_type, DATE_COLUMN_NAME])
        data = data.append(series, ignore_index=True)

    print(f"Successfully added {item}.")
    print()
    return data


def add_details(data):
    print("adding details not yet implemented")


def add_new_values(data, decision_type):
    date = input("What date are these values for? ")
    while True:
        item = input("Enter an item or back: ")
        if item.lower() == "back":
            break

        quantity = input("Enter a quantity or cancel: ")
        if quantity.lower() == "cancel":
            continue

        data = _add_value(data, date, item, quantity, decision_type)

    return data


def start():
    decision_type = _confirm_input(
        input("Modifying drops or kills? "), ["drops", "kills"])
    # Set up the data
    data = pd.read_csv(f"{decision_type}.csv")
    _process_dates(data)

    decision = _confirm_input(
        input("Adding details or adding new values? "),
        ["details", "new values"])
    if decision == "details":
        add_details(data)
    else:
        data = add_new_values(data, decision_type[:-1])

    # Save the data
    _unprocess_dates(data)
    data.to_csv(f"{decision_type}.csv", index=False)


if __name__ == "__main__":
    start()
