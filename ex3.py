#!/usr/bin/env python3
"""ex3.py
Author: Omar Amr
Matr.Nr.: K11776960
Exercise 3
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import pickle
import pathlib
from ex1 import scan_directory
from ex2 import read_file_content

arg = sys.argv[1]  # input from the command line.


def read_all_files(directory=arg):
    directory = directory.rstrip('/')
    files = scan_directory(directory)  # get the list of files with .exp1.data extension using ex1 functions.

    if len(files) == 0:
        print("No files found!")
        return

    values = {}  # dictionary to store the mean age per experiment. keys are experiment No., Values are mean age.
    heights = []  # list to store all height values. used to write data as pkl file.
    print("\n")

    # loop through all the detected files to extract the required data.
    for file in files:
        try:
            # get age and height values from the file using ex2 functions
            file_output = read_file_content(file, ["age", "height"])
            experiment_number = file_output[0]
            columns_values = file_output[1]
            # calculate mean age per current file.
            age_mean = sum(columns_values["age"]) * 1.0 / len(columns_values["age"])
            heights += (columns_values["height"])  # append heights of current file to the list containing all heights.

            # if the experiment number of this file was detected before, calculate the mean over all age values.
            if experiment_number in values:
                values[experiment_number] = (values[experiment_number] + age_mean) / 2
            else:
                # If experiment number never detected before, create a new key in the dictionary and store mean age.
                values[experiment_number] = age_mean

        except (AttributeError, ValueError):
            # if the file is not correct, the error is ignored and a corresponding notification message is displayed.
            print("Invalid file [{}] found but ignored!".format(file))

    output_directory = directory + "_processed"  # define the output directory path.

    values = dict(sorted(values.items()))  # sort dictionary by experiment number.
    pathlib.Path(output_directory).mkdir(parents=True, exist_ok=True)  # create the output directory on the file system.

    # convert keys and values of the dictionary to lists to be used in the plotting function.
    experiment_numbers = list(map(int, list(values.keys())))
    experiment_age_means = list(values.values())

    fig = plt.figure(figsize=(7, 7))  # resize the graph for better visualization.
    ax = fig.add_subplot(111)
    ax.set_xticks(experiment_numbers)  # set the values on x-axis to show experiments numbers.
    plt.plot(experiment_numbers, experiment_age_means)  # plotting the experiment number vs. the mean age graph.
    plt.tight_layout(pad=2)  # removing surrounding white space around the graph.
    plt.margins(0.1, 0.12)

    for i in values:
        x = int(i)
        y = float("{0:.2f}".format(values[i]))
        # show the mean average on the plot next to its corresponding experiment number.
        plt.annotate(y, xy=(x, y), xytext=(x, y + 1.5), arrowprops=dict(arrowstyle="-|>", color='red'))

    plt.xlabel("Experiment")  # setting the label of x-axis.
    plt.ylabel("Age")  # setting the label of y-axis.
    plt.title("Average age")  # setting the title of the graph.
    plt.savefig(output_directory + "/average_age.png")  # save the graph as png image in the output directory.

    # flaot32 was supposed to be used, however it changes the values of the original heights array after conversion.
    # So float64 was used instead to maintain the same values as the original array.
    heights = np.asarray(heights, dtype=np.float64)  # convert the list of heights to numpy array.

    # write the heights numpy array to the output directory
    pickle.dump(heights, open(output_directory + "/heights.pkl", "wb"))

    print("\nEx 3 is done!")


if __name__ == "__main__":
    read_all_files()
