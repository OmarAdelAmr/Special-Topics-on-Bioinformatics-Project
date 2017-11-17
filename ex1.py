import os


def scan_directory(directory):
    files_counter = 0
    found_files = []

    for folder in os.walk(os.path.abspath(os.path.expanduser(directory))):
        for file in folder[2]:
            if file.endswith(".exp1.data"):
                file_full_path = folder[0] + "/" + file
                print(file_full_path)
                found_files.append(file_full_path)
                files_counter += 1

    print("\nNumber of files: " + str(files_counter))
    return found_files


directory1 = "~/Desktop/Special-Topics-on-Bioinformatics-Project/Test Folder"
directory2 = "/Users/omaramr/Desktop/Special-Topics-on-Bioinformatics-Project/Test Folder"

file_names_list = scan_directory(directory2)
