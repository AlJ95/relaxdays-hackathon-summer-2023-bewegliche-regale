
import json

from constants import INPUT_DIR


def load_json(filename):
    with open(INPUT_DIR / filename, encoding="utf-8") as file:
        data = json.load(file)
    return data


def shortest_path(start, end, non_movables):
    pass
