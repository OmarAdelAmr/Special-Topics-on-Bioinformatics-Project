import sys
import math
import pickle
import matplotlib.pyplot as plt
import numpy as np
from subprocess import call


arg1 = sys.argv[1]


def shell_script(directory=arg1):
    call(["python3", "ex3.py", directory])

    output_directory = directory + "_processed/"

    heights = pickle.load(open(output_directory + "heights.pkl", "rb"))

    bin_upper_bound = math.ceil(np.amax(heights)) + 1
    print(bin_upper_bound)
    n_bins = range(0, bin_upper_bound)

    arr = plt.hist(heights, n_bins, histtype='bar', edgecolor='white', color="red")

    for i in range(0, bin_upper_bound - 1):
        if arr[0][i] != 0:
            plt.text(arr[1][i], arr[0][i], str(int(arr[0][i])), rotation=90)

    plt.title("Heights")
    plt.savefig(output_directory + "/heights.png")

    print("\nEx 4 is Done")


if __name__ == "__main__":
    shell_script()
