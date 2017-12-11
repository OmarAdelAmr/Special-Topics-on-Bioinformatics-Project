#!/usr/bin/env python3
"""ex4.py
Author: Omar Amr
Matr.Nr.: K11776960
Exercise 4
"""

import sys
import math
import pickle
import matplotlib.pyplot as plt
import numpy as np
from subprocess import call

arg1 = sys.argv[1]  # input from the command line.


def shell_script(directory=arg1):
    directory = directory.rstrip('/')
    call(["python3", "ex3.py", directory])

    output_directory = directory + "_processed/"  # define the output directory path.

    heights = pickle.load(open(output_directory + "heights.pkl", "rb"))  # Load the heights.pkl that was saved in ex3.

    # the upper bound for the pins in the histogram is equal to the maximum height in the file + 1.
    bin_upper_bound = math.ceil(np.amax(heights)) + 1
    n_bins = np.arange(0.0, bin_upper_bound, 0.1)  # pins in the histogram from 0 to the upper bound of bins.

    fig = plt.figure(figsize=(25, 15))  # resize the size of the graph for better visualization.
    ax = fig.add_subplot(111)
    ax.set_xticks(np.arange(len(n_bins)))  # setting the values of x axis to the bins defined above.
    arr = plt.hist(heights, n_bins, histtype='bar', color="red")  # plotting the histogram.
    plt.tight_layout(pad=2)  # removing surrounding white space around the graph.

    for i in range(0, arr[0].size):
        if arr[0][i] != 0:
            # display the number of occurrences per each histogram bin.
            plt.text(arr[1][i] - 0.13, arr[0][i] + 0.05, str(int(arr[0][i])), rotation=0, fontsize=13)

    plt.title("Heights")  # set the title of the graph
    plt.savefig(output_directory + "/heights.png")  # save the graph as png image in the output directory.

    print("\nEx 4 is done!")


if __name__ == "__main__":
    shell_script()
