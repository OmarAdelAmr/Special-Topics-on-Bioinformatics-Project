import os


def scan_directory(directory):
    files_counter = 0
    found_files = []

    for folder in os.walk(os.path.abspath(os.path.expanduser(directory))):
        for file in folder[2]:
            if file.endswith(".exp1.data"):
                file_full_path = folder[0] + "/" + file
                found_files.append(file_full_path)
                files_counter += 1

    return found_files


if __name__ == "__main__":
    directory = "/Users/omaramr/Desktop/Special-Topics-on-Bioinformatics-Project"

    file_names_list = scan_directory(directory)
    for file in file_names_list:
        print(file)
    print("\nNumber of files: {}".format(len(file_names_list)))
