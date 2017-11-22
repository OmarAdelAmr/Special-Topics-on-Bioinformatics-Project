# TODO: Understand exactly when each Error should be raised
# TODO: Value error not done yet
# If no lines where all desired values exist can be found, your function
# should raise a ValueError.


# TODO: Is order important?
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


def get_columns_data(separated_lines):
    try:
        data_start_index = separated_lines.index("# Data start")
    except ValueError:
        raise AttributeError("TODO: file ends before any data is presented") from None

    data_end_index = separated_lines[data_start_index:].index("# Data end") + data_start_index
    columns_data = separated_lines[data_start_index + 1: data_end_index]
    split_columns_data = []
    for x in columns_data:
        split_columns_data.append(x.split())

    print(type(split_columns_data))
    return split_columns_data


def get_columns_names(separated_lines):
    y = [x for x in separated_lines if x.startswith("# Columns")]
    column_names = []
    if len(y) != 0:
        for x in y:
            column_string = x.replace("# Columns:", "")
            column_names = column_string.lower().split()
    return column_names


def get_experiment_number(separated_lines):
    y = [x for x in separated_lines if x.startswith("# Experiment")]
    experiment_number = 0
    if len(y) != 0:
        for x in y:
            experiment_number = x.replace("# Experiment:", "")

    return experiment_number


def read_file_content(file_name, columns_list):
    file_content = open(file_name, 'r').read()
    separated_lines = file_content.splitlines()
    # TODO: replace condition with any number of spaces
    separated_lines = [x for x in separated_lines if x != ""]

    try:
        separated_lines = separated_lines[:separated_lines.index("# Data end") + 1]
    except ValueError:
        raise AttributeError("'# Data end' was not found") from None

    validate_header(separated_lines)
    column_names = get_columns_names(separated_lines)
    column_values = get_columns_data(separated_lines)
    experiment_number = get_experiment_number(separated_lines)
    values = {}
    for column in columns_list:
        column_lower = column.lower()
        try:
            values[column] = [item[column_names.index(column_lower)] for item in column_values]
        except ValueError:
            raise AttributeError("Column '" + column + "' is not defined") from None

    print("\n" + "Experiment number:", experiment_number + "\n")

    for x in values:
        print(x, "values:", values[x])

    return experiment_number, values


# read_file_content("Test Folder/test5.exp1.data", ['index', 'height', 'age'])
read_file_content("correct.exp1.data", ['HEIGHT', 'NoRm'])
# print(read_file_content("example_file.exp1.data", ['Index', 'height', 'AG']))

# TODO: Errors and Convert values to double
