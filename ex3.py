import sys
import matplotlib.pyplot as plt
import numpy as np
import pickle
import pathlib

from ex1 import scan_directory
from ex2 import read_file_content

arg = sys.argv[1]


def read_all_files(directory=arg):
    files = scan_directory(directory)

    if len(files) == 0:
        print("No files found!")
        return

    values = {}  # (Exp No.): [mean age]
    heights = []
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

    experiment_numbers = list(map(int, list(values.keys())))
    experiment_age_means = list(values.values())

    plt.plot(experiment_numbers, experiment_age_means)
    plt.xlabel("Experiment")
    plt.ylabel("Age")
    plt.title("Average age")
    plt.savefig(output_directory + "/average_age.png")

    heights = np.asarray(heights, dtype=np.float32)
    pickle.dump(heights, open(output_directory + "/heights.pkl", "wb"))

    print("\nEx 3 is done!")


if __name__ == "__main__":
    read_all_files()
