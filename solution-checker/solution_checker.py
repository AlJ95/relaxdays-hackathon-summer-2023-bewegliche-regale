import os
import json


def process_package(current: str, incoming: str) -> str:
    if current in "🙋‍👷":
        return "👷" if incoming in "📦👷" else "🙋"
    else:
        if incoming in "📦👷":
            return "📦"
    return "🎁"


def apply_step(lager, step):
    next_lager = [["" for _ in row] for row in lager]
    pre_step_validation(lager, step)
    for row in range(len(lager)):
        for col in range(len(lager[row])):
            if step[row][col] != "🟨":
                if lager[row][col] == '👷':
                    next_lager[row][col] = "🙋"
            if row > 0 and step[row - 1][col] == "⏬":
                next_lager[row][col] += process_package(lager[row][col], lager[row - 1][col])
            if row < len(lager) - 1 and step[row + 1][col] == "⏫":
                next_lager[row][col] += process_package(lager[row][col], lager[row + 1][col])
            if col > 0 and step[row][col - 1] == "⏩":
                next_lager[row][col] += process_package(lager[row][col], lager[row][col - 1])
            if col < len(lager[row]) - 1 and step[row][col + 1] == "⏪":
                next_lager[row][col] += process_package(lager[row][col], lager[row][col + 1])
            if step[row][col] == "🟨":
                next_lager[row][col] += lager[row][col]
            if next_lager[row][col] == "🙋🙋":
                next_lager[row][col] = "🙋"
            if next_lager[row][col] == "🙋👷" or next_lager[row][col] == "👷🙋":
                next_lager[row][col] = "👷"
            if len(next_lager[row][col]) == 2:
                next_lager[row][col] = next_lager[row][col].replace("🟨", "")

            if len(next_lager[row][col]) > 1:
                raise Exception("Can't move because packages would crash")
    return ["".join(c if c != "" else "🟨" for c in next_row) for next_row in next_lager]


def pre_step_validation(lager, step):
    for row in range(len(lager)):
        for col in range(len(lager[row])):
            if step[row][col] != "🟨":
                if lager[row][col] not in "📦🎁👷‍️":
                    raise Exception("Can't move without package.")
                if step[row][col] == "⏬" and (row == len(lager) - 1 or step[row + 1][col] not in "🟨⏬"):
                    raise Exception(
                        "Can't move down, because that package is moving in a different direction or its out of "
                        "bounds")
                if step[row][col] == "⏪" and (col == 0 or step[row][col - 1] not in "🟨⏪"):
                    raise Exception(
                        "Can't move left, because that package is moving in a different direction or its out of "
                        "bounds")
                if step[row][col] == "⏫" and (row == 0 or step[row - 1][col] not in "🟨⏫"):
                    raise Exception(
                        "Can't move up, because that package is moving in a different direction or its out of "
                        "bounds")
                if step[row][col] == "⏩" and (col == len(lager[row]) - 1 or step[row][col + 1] not in "🟨⏩"):
                    raise Exception(
                        "Can't move right, because that package is moving in a different direction or its out "
                        "of bounds")
                if step[row][col] == "⏬" and lager[row + 1][col] in "📦🎁👷‍️" and step[row + 1][col] == "🟨":
                    raise Exception("Can't move down, because the package would crash")
                if step[row][col] == "⏪" and lager[row][col - 1] in "📦🎁👷‍️" and step[row][col - 1] == "🟨":
                    raise Exception("Can't move left, because the package would crash")
                if step[row][col] == "⏫" and lager[row - 1][col] in "📦🎁👷‍️" and step[row - 1][col] == "🟨":
                    raise Exception("Can't move up, because the package would crash")
                if step[row][col] == "⏩" and lager[row][col + 1] in "📦🎁👷‍️" and step[row][col + 1] == "🟨":
                    raise Exception("Can't move right, because the package would crash")


def apply_instructions(lager: list[str], instructions: list[list[str]]) -> list[str]:
    for step in instructions:
        try:
            lager = apply_step(lager, step)
        except Exception:
            return None

    return lager


def check_solution(lager: list[str], instructions: list[list[str]]):
    final_lager = apply_instructions(lager, instructions)
    if not final_lager:
        return False
    return "🎁" not in "".join(final_lager)


def main():
    input_folder = "input"
    output_folder = "output"

    input_files = os.listdir(input_folder)
    output_files = os.listdir(output_folder)

    for input_file, output_file in zip(input_files, output_files):
        with open(os.path.join(input_folder, input_file), "r") as f:
            lager = json.load(f)

        with open(os.path.join(output_folder, output_file), "r") as f:
            instructions = json.load(f)

        is_valid = check_solution(lager, instructions)
        print(f"{input_file}: {'Valid' if is_valid else 'Invalid'}, "
              f"{len(instructions)} steps, "
              f"{sum(len(i)*len(i[0]) - ''.join(i).count('🟨') for i in instructions)}")


if __name__ == "__main__":
    main()
