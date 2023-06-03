
from pathlib import Path


INPUT_DIR = Path("./solution-checker/input")
OUTPUT_DIR = Path("./solution-checker/output")


class Symbol:

    EMPTY = "🟨"
    BUSY_WORKER = "👷"
    IDLE_WORKER = "🙋"
    PACKAGE = "📦"
    ORDERED_PACKAGE = "🎁"

    DOWN = "⏬"
    LEFT = "⏪"
    RIGHT = "⏩"
    UP = "⏫"
