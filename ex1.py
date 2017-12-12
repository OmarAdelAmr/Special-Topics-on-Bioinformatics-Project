#!/usr/bin/env python3
"""ex1.py
Author: Omar Amr
Matr.Nr.: K11776960
Exercise 1
"""

import os


def scan_directory(directory):
    found_files = []  # a list that stores the paths of files with .exp1.data extension.

    # detects all folders in specified directory including base level (the directory itself).
    for folder in os.walk(os.path.abspath(os.path.expanduser(directory))):  # use absolute path.
        for file in folder[2]:  # loop through all files in a specific folder.
            if file.endswith(".exp1.data"):
                # if the current file has .exp1.data extension, store its path in the list of found_files defined above.
                file_full_path = folder[0] + "/" + file
                found_files.append(file_full_path)

    return found_files


if __name__ == "__main__":
    input_directory = "/Users/omaramr/Desktop/Special-Topics-on-Bioinformatics-Project"
    file_names_list = scan_directory(input_directory)

    for file_name in file_names_list:  # loop through found files for printing their paths
        print(file_name)
    print("\nNumber of files: {}".format(len(file_names_list)))  # print number of found files
