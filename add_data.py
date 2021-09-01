from util import TextFormat
from util import confirm_input
from util import process_dates_from_dict
from util import process_dates_from_string

import pandas as pd


DATE_COLUMN_NAME = "dates"
TESTING = True


def _add_value(data, date, item, quantity, item_type):
    if item in data[item_type].values:
        existing_dict = data.loc[
            data.index[data[item_type] == item]][DATE_COLUMN_NAME].item()
        existing_dict[date] = quantity
    else:
        series = pd.Series(
            data={
                item_type: item,
                DATE_COLUMN_NAME: {date: quantity}},
            index=[item_type, DATE_COLUMN_NAME])
        data = data.append(series, ignore_index=True)

    print(f"Successfully added {item}.")
    return data


def _save_info(data, rowIdx, columnName, questionString):
    input_value = input(questionString)
    if input_value == "back":
        return False
    if input_value == "continue":
        return True
    data.at[rowIdx, columnName] = input_value
    return True


def _collect_info_drop(data, existing_value):
    info1 = "category"
    info2 = "average_worth"
    type_col_name = "drop"
    existing_idx = data.index[
        data[type_col_name] == existing_value[type_col_name].item()
    ].tolist()[0]

    data[info1] = data[info1].astype(str)

    if not _save_info(data, existing_idx, info1,
                      f"\tWhat is the {TextFormat.BLUE}category"
                      f"{TextFormat.END}? "):
        return False
    return _save_info(data, existing_idx, info2,
                      f"\tWhat is the {TextFormat.BLUE}average worth"
                      f"{TextFormat.END}? ")


def _collect_info_kill(data, existing_value):
    info1 = "level"
    info2 = "category"
    type_col_name = "kill"
    existing_idx = data.index[
        data[type_col_name] == existing_value[type_col_name].item()
    ].tolist()[0]

    data[info2] = data[info2].astype(str)

    if not _save_info(data, existing_idx, info1,
                      f"\tWhat is the {TextFormat.BLUE}level"
                      f"{TextFormat.END}? "):
        return False
    return _save_info(data, existing_idx, info2,
                      f"\tWhat is the {TextFormat.BLUE}category"
                      f"{TextFormat.END}? ")


def collect_information(data, existing_value, item_type):
    if item_type == "drop":
        return _collect_info_drop(data, existing_value)
    return _collect_info_kill(data, existing_value)


def add_details(data, item_type):
    missing_info = data[data.isnull().any(axis=1)].sort_values(by=[item_type])
    for index, row in missing_info.iterrows():
        print()
        existing_value = data.loc[
            data.index[data[item_type] == row[item_type]]]
        print(
            f"Entering information for {TextFormat.BOLD}"
            f"{row[item_type]}{TextFormat.END}")
        if not collect_information(data, existing_value, item_type):
            return


def add_new_values(data, decision_type):
    date = input(f"What {TextFormat.BLUE}date{TextFormat.END} "
                 "are these values for? ")
    while True:
        print()
        item = input(f"Enter an {TextFormat.BLUE}item{TextFormat.END} "
                     "or back: ")
        if item.lower() == "back":
            break

        quantity = input(f"Enter a {TextFormat.BLUE}quantity{TextFormat.END} "
                         "or cancel: ")
        if quantity.lower() == "cancel":
            continue

        data = _add_value(data, date, item, quantity, decision_type)

    return data


def start():
    decision_type = confirm_input(
        input(f"Modifying {TextFormat.GREEN}drops{TextFormat.END} "
              f"or {TextFormat.GREEN}kills{TextFormat.END}? "),
        ["drops", "kills"])
    # Set up the data
    filename = (f"test_data/{decision_type}.csv" if TESTING
                else f"{decision_type}.csv")
    data = pd.read_csv(filename)
    process_dates_from_string(data)

    decision = confirm_input(
        input(f"Adding {TextFormat.GREEN}details{TextFormat.END} "
              f"or adding {TextFormat.GREEN}new values{TextFormat.END}? "),
        ["details", "new values"])
    if decision == "details":
        add_details(data, decision_type[:-1])
    else:
        data = add_new_values(data, decision_type[:-1])

    # Save the data
    process_dates_from_dict(data)
    data.to_csv(filename, index=False)


if __name__ == "__main__":
    start()
