#!/usr/bin/env python3
"""ex2.py
Author: Omar Amr
Matr.Nr.: K11776960
Exercise 2
"""

import numpy as np


def validate_header(separated_lines):
    try:
        header_start_index = separated_lines.index("# Header Start")
        separated_lines = separated_lines[header_start_index + 1:header_start_index + 4]
    except ValueError:
        raise AttributeError("Header not valid, '# Header Start' not found") from None

    validation_check_array = [False, False, False]
    for x in separated_lines:
        if x.startswith("# Experiment:"):
            validation_check_array[0] = True
        elif x.startswith("# Columns:"):
            validation_check_array[1] = True
        elif x == "# Data start":
            validation_check_array[2] = True

    if not validation_check_array[0]:
        raise AttributeError("Header not valid, 'Experiment Number' not found") from None
    elif not validation_check_array[1]:
        raise AttributeError("Header not valid, No columns found") from None
    elif not validation_check_array[2]:
        raise AttributeError("Header not valid, 'Data start' not found") from None


def get_required_columns_data(separated_lines, columns_indices, columns_names):
    try:
        data_start_index = separated_lines.index("# Data start")
    except ValueError:
        raise AttributeError("'# Data end' is triggered before any data is presented") from None

    data_end_index = separated_lines[data_start_index:].index("# Data end") + data_start_index
    columns_data = separated_lines[data_start_index + 1: data_end_index]

    if len(columns_data) == 0:
        raise ValueError("No values exist") from None

    columns_data = [x.split() for x in columns_data]
    float_columns_data = []

    for row in columns_data:
        try:
            float_columns_data.append([float(x) for x in np.array(row)[columns_indices]])
        except IndexError:
            raise AttributeError("Some columns have missing values in input data file.") from None
        except ValueError:
            pass

    result_dict = {}

    for i in range(len(columns_names)):
        result_dict[columns_names[i]] = [item[i] for item in float_columns_data]

    return result_dict


def get_all_columns_names(separated_lines):
    y = [x for x in separated_lines if x.startswith("# Columns")]
    column_names = []
    if len(y) != 0:
        for x in y:
            column_string = x.replace("# Columns:", "")
            column_names = column_string.lower().split()

    return column_names


def get_experiment_number(separated_lines):
    y = [x for x in separated_lines if x.startswith("# Experiment")]
    experiment_number = ""
    if len(y) != 0:
        for x in y:
            experiment_number = x.replace("# Experiment:", "")

    try:
        experiment_number = int(experiment_number)
    except ValueError:
        error_message = "Header not valid, "
        if str(experiment_number).strip() == "":
            error_message += "Experiment Number not found"
        else:
            error_message += "Invalid Experiment Number format. Non numeric value"
        raise AttributeError(error_message) from None

    return experiment_number


def read_file_content(file_name, columns_list):
    file_content = open(file_name, 'r').read()
    separated_lines = file_content.splitlines()
    separated_lines = [x for x in separated_lines if x.strip() != ""]

    try:
        separated_lines = separated_lines[:separated_lines.index("# Data end") + 1]
    except ValueError:
        raise AttributeError("'# Data end' was not found") from None

    validate_header(separated_lines)
    column_names = get_all_columns_names(separated_lines)
    try:
        required_columns_indices = [column_names.index(x.lower()) for x in columns_list]
    except ValueError:
        raise AttributeError("Input Column Not Defined") from None  # TODO: Add which column causes error

    values = get_required_columns_data(separated_lines, required_columns_indices, columns_list)
    experiment_number = get_experiment_number(separated_lines)

    return experiment_number, values


if __name__ == "__main__":
    directory = "correct.exp1.data"  # "correct.exp1.data"
    required_columns = ['INDEX', 'heiGht', 'descriptioN']
    result = read_file_content(directory, required_columns)
    print("\nExperiment Number: {} \n".format(result[0]))

    for column_value in result[1]:
        print(column_value, ":", result[1][column_value])
