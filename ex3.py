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

arg = sys.argv[1]


def read_all_files(directory=arg):
    directory = directory.rstrip('/')
    files = scan_directory(directory)

    if len(files) == 0:
        print("No files found!")
        return

    values = {}  # (Exp No.): [mean age]
    heights = []
    print("\n")
    for file in files:
        try:
            file_output = read_file_content(file, ["age", "height"])
            experiment_number = file_output[0]
            columns_values = file_output[1]
            age_mean = sum(columns_values["age"]) * 1.0 / len(columns_values["age"])
            heights += (columns_values["height"])

            if experiment_number in values:
                values[experiment_number] = (values[experiment_number] + age_mean) / 2
            else:
                values[experiment_number] = age_mean

        except (AttributeError, ValueError):
            print("Invalid file [{}] found but ignored!".format(file))

    output_directory = directory + "_processed"

    values = dict(sorted(values.items()))  # sort dictionary by experiment number
    pathlib.Path(output_directory).mkdir(parents=True, exist_ok=True)

    # TODO: Handle if experiment number does not exist. e.g. # Experiment: <Non numeric value>
    experiment_numbers = list(map(int, list(values.keys())))
    experiment_age_means = list(values.values())

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111)
    ax.set_xticks(experiment_numbers)
    plt.plot(experiment_numbers, experiment_age_means)
    plt.tight_layout(pad=2)
    plt.margins(0.1, 0.12)

    for i in values:
        x = int(i)
        y = float("{0:.2f}".format(values[i]))
        plt.annotate(y, xy=(x, y), xytext=(x, y + 1.5), arrowprops=dict(arrowstyle="-|>", color='red'))

    plt.xlabel("Experiment")
    plt.ylabel("Age")
    plt.title("Average age")
    plt.savefig(output_directory + "/average_age.png")

    # TODO: Originally float32, waiting for answer to see if should be changed.
    heights = np.asarray(heights, dtype=np.float64)
    pickle.dump(heights, open(output_directory + "/heights.pkl", "wb"))

    print("\nEx 3 is done!")


if __name__ == "__main__":
    read_all_files()
