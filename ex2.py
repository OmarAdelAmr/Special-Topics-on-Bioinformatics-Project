def get_columns_data(separated_lines):
    data_start_index = separated_lines.index("# Data start")
    data_end_index = separated_lines[data_start_index:].index("# Data end") + data_start_index
    columns_data = separated_lines[data_start_index + 1: data_end_index]
    split_columns_data = []
    for x in columns_data:
        split_columns_data.append(x.split())
    return split_columns_data


def get_columns_names(separated_lines):
    y = [x for x in separated_lines if x.startswith("# Columns")]
    column_names = []
    if len(y) != 0:
        for x in y:
            column_string = x.replace("# Columns:", "")
            column_names = column_string.lower().split()
    return column_names


def read_file_content(file_name, columns_list):
    file_content = open(file_name, 'r').read()
    separated_lines = file_content.splitlines()
    column_names = get_columns_names(separated_lines)
    column_values = get_columns_data(separated_lines)
    result = {}
    for column in columns_list:
        column_lower = column.lower()
        result[column] = [item[column_names.index(column_lower)] for item in column_values]

    print(result)
    return result


read_file_content("example_file.exp1.data", ['Index', 'height', 'age', 'description'])

# TODO Errors and Convert values to double
