#!/usr/bin/env python3
"""ex2.py
Author: Omar Amr
Matr.Nr.: K11776960
Exercise 2
"""

import numpy as np


# This function makes sure that the header is valid and has no missing values.
# It also extracts the experiment number from the header and all column names in the header.
def validate_header(separated_lines):
    try:
        # find the position of '# Header Start' line, and find the 4 lines that form a valid header.
        header_start_index = separated_lines.index("# Header Start")
        separated_lines = separated_lines[header_start_index + 1:header_start_index + 4]
    except ValueError:
        # raise exception if header start not found in the file.
        raise AttributeError("Header not valid, '# Header Start' not found or data ends before header.") from None

    # check if any header value is missing and show a customized error message based in that.
    validation_check_array = [False, False, False]
    experiment_number = ""
    columns_names = ""
    for x in separated_lines:
        if x.startswith("# Experiment:"):
            validation_check_array[0] = True
            experiment_number = x.replace("# Experiment:", "").strip()
        elif x.startswith("# Columns:"):
            validation_check_array[1] = True
            columns_names = (x.replace("# Columns:", "")).lower().split()
        elif x == "# Data start":
            validation_check_array[2] = True

    # raise exceptions with customized error message to define what is exactly wrong with the header.
    if not validation_check_array[0]:
        raise AttributeError("Header not valid, 'Experiment Number' not found.") from None
    elif not validation_check_array[1]:
        raise AttributeError("Header not valid, No columns found.") from None
    elif not validation_check_array[2]:
        raise AttributeError("Header not valid, 'Data start' not found.") from None

    try:
        float(experiment_number)  # check that experiment number is a numeric value, raise exception otherwise.
    except ValueError:
        raise AttributeError("Invalid Experiment Number. Non numeric value.") from None

    return experiment_number, columns_names


# This function gets the data of required columns, and assures that only float values are returned.
# It returns a dictionary containing the required column names as keys and its corresponding values as values.
def get_required_columns_data(separated_lines, columns_indices, columns_names):
    data_start_index = separated_lines.index("# Data start")  # get the position of '# Data start' in the file.
    data_end_index = separated_lines.index("# Data end")  # get the position of '# Data end' in the file.
    columns_data = separated_lines[data_start_index + 1: data_end_index]  # get all values of columns.

    if len(columns_data) == 0:  # check that values exist between '# Data start' and '# Data end'
        raise ValueError("No values exist") from None

    columns_data = [x.split() for x in columns_data]  # split values of each line on whitespaces to a list.
    float_columns_data = []  # stores values of required columns if these values can be converted to numeric values.

    for row in columns_data:
        try:
            # get only the values of required columns and try to convert them into numeric values.
            # If conversion succeeds for all values, these values are appended to the float_columns_data list.
            float_columns_data.append([float(x) for x in np.array(row)[columns_indices]])
        except IndexError:
            raise AttributeError("Some columns have missing values in input data file.") from None
        except ValueError:
            # If any value in a line cannot be converted to float, the whole line is ignored.
            pass

    result_dict = {}  # this dictionary is used to store the final values with their column name as key.

    for i in range(len(columns_names)):
        result_dict[columns_names[i]] = [item[i] for item in float_columns_data]

    return result_dict


# This function takes the input file name and the required columns and calls helper methods defined above.
# It returns the experiment number and a dictionary with desired values.
def read_file_content(file, columns_list):
    file_content = open(file, 'r').read()  # open the input file.
    separated_lines = file_content.splitlines()  # separate the file's content to list of lines.
    separated_lines = [x for x in separated_lines if x.strip() != ""]  # ignore empty lines(including whitespace lines).

    try:
        # ignore any lines that come after "# Data end" line, and raise an error if the line was never found.
        separated_lines = separated_lines[:separated_lines.index("# Data end") + 1]
    except ValueError:
        raise AttributeError("'# Data end' not found.") from None

    header_values = validate_header(separated_lines)  # make sure the header is valid.
    experiment_number = header_values[0]  # get the experiment number of the input file.
    column_names = header_values[1]  # get all columns names in the input file.

    if len(column_names) == 0:  # raise error if inout file has no column names.
        raise AttributeError("No columns found in input file.") from None

    try:
        # get the corresponding index for each column in the input with respect to its location in the file.
        # know the position of each column.
        required_columns_indices = [column_names.index(x.lower()) for x in columns_list]
    except ValueError:
        # if the list of input columns has a column name that does not exist in the file, an exception is raised.
        raise AttributeError("Entered column/s not defined, check input column names") from None

    # create a dictionary with column names as keys and the returned values from the file as values of the dictionary.
    values = get_required_columns_data(separated_lines, required_columns_indices, columns_list)

    return experiment_number, values


if __name__ == "__main__":
    file_name = "correct.exp1.data"
    required_columns = ['INDEX', 'heiGht', 'descriptioN']
    result = read_file_content(file_name, required_columns)

    print("\nExperiment Number: {} \n".format(result[0]))

    for column_value in result[1]:  # loop through dictionary to print each key with its corresponding values.
        print(column_value, ":", result[1][column_value])
