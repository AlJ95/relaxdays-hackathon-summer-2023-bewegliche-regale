import sys
import time
from pathlib import Path
from sklearn.metrics.pairwise import manhattan_distances
from constants import *
import numpy as np
import json

DATA_DIRECTORY = Path('./solution-checker/input')
FILENAME = 'instance{i}.json'


def load_json(i) -> np.ndarray:
    """
    Loads one of the json files from the data directory.
    :param i: the number of the file to load
    :return: the data from the file
    """
    with open(DATA_DIRECTORY / FILENAME.format(i=i), encoding="utf-8") as f:
        data = np.array(json.load(f))
    return data


def print_data(data: np.ndarray):
    """
    Prints the data in a nice way
    :param data: the data to print
    """
    for row in data:
        print(row)


def animate_solution(data: list[np.ndarray]):
    """
    Animates the solution in the terminal
    :param data: the solution to animate
    """
    for solution in data:
        for row in solution:
            sys.stdout.write("\r" + row)
        time.sleep(0.5)
        sys.stdout.flush()


if __name__ == '__main__':
    input_data = load_json(0)
    print_data(input_data)


"""
📦📦📦📦📦📦📦
📦📦🟨🎁📦📦🙋
📦📦⏫📦📦📦📦
"""
"""
📦📦📦📦📦📦📦
📦📦📦🎁📦📦🙋
📦📦🟨⏪⏪📦📦
"""
"""
📦📦📦📦📦📦📦
📦📦📦🎁⏬📦🙋
📦📦📦📦🟨📦📦
"""
"""
📦📦📦📦📦📦📦
📦📦📦⏩🟨📦🙋
📦📦📦📦📦📦📦
"""
"""
📦📦📦📦📦📦📦
📦📦📦🟨🎁📦🙋
📦📦📦📦📦📦📦
"""