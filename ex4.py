import sys
import math
import pickle
import matplotlib.pyplot as plt
import numpy as np

from subprocess import call

arg1 = sys.argv[1]


# TODO: Revision Still Needed, Specially Plots.
# TODO: Revision, where the output directory should be.

def shell_script(directory=arg1):
    directory = directory.rstrip('/')
    call(["python3", "ex3.py", directory])

    output_directory = directory + "_processed/"

    heights = pickle.load(open(output_directory + "heights.pkl", "rb"))

    bin_upper_bound = math.ceil(np.amax(heights)) + 1
    n_bins = np.arange(0.0, bin_upper_bound, 0.1)

    fig = plt.figure(figsize=(25, 15))
    ax = fig.add_subplot(111)
    ax.set_xticks(np.arange(len(n_bins)))
    arr = plt.hist(heights, n_bins, histtype='bar', color="red")
    plt.tight_layout(pad=2)

    for i in range(0, arr[0].size):
        if arr[0][i] != 0:
            # TODO: Add height value on graph for each bar. Next Line
            # bin_label = "Count({}) = {}".format(str(float(arr[1][i])), str(int(arr[0][i])))
            plt.text(arr[1][i], arr[0][i], str(int(arr[0][i])), rotation=0, fontsize=15)

    plt.title("Heights")
    plt.savefig(output_directory + "/heights.png")

    print("\nEx 4 is done!")


if __name__ == "__main__":
    shell_script()
