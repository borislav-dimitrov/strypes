import os.path
import sys


def read_whole_file(file):
    with open(file, "rt", encoding="utf-8") as f:
        lines = f.readlines()

    return lines


def r_file_and_prep_info(file):
    file_info = read_whole_file(file)
    file_info = [f.strip() for f in file_info if f.strip() != ""]
    tests = file_info.pop(0)
    task = {
        "tests": tests,
        "cases": []
    }
    row = 0
    while row < len(file_info):
        height = file_info[row].split(" ")[0]
        width = file_info[row].split(" ")[1]
        board_range = [i + 1 for i in range(row, row + int(height))]
        board = [item for item in [file_info[r] for r in board_range]]
        task["cases"].append({"height": height, "width": width, "board": board})
        row += int(height) + 1
    return task


def move_bot_to(row, col, board, direction):
    # Тук row и col не би ли следвало да са референции към подадените параметри ?
    # Докато не ги включих в return клаузата не се променяха.
    if direction == "r":
        col += 1
    elif direction == "l":
        col -= 1
    elif direction == "u":
        row -= 1
    elif direction == "d":
        row += 1
    return board[row][col], row, col


def test_starting_point(board, r, c, rows, columns):
    passed_through = []
    row = r
    col = c
    curr_cell = board[r][c]

    try:
        while (row, col) not in passed_through:  # Robot shutdown
            passed_through.append((row, col))

            if curr_cell.lower() == "r":
                curr_cell, row, col = move_bot_to(row, col, board, "r")
            elif curr_cell.lower() == "l":
                curr_cell, row, col = move_bot_to(row, col, board, "l")
            elif curr_cell.lower() == "u":
                curr_cell, row, col = move_bot_to(row, col, board, "u")
            elif curr_cell.lower() == "d":
                curr_cell, row, col = move_bot_to(row, col, board, "d")

            if row < 0 or col < 0 or row > rows - 1 or col > columns - 1:
                # Robot fell  off the table
                break

    except IndexError as ex:
        # Robot fell off the table
        return [r + 1, c + 1, len(passed_through) + 1]
    except Exception as ex:
        print("Ooops!", type(ex), ex)
    finally:
        return [r + 1, c + 1, len(passed_through)]


def format_tests(tests):
    answer = []
    for test in tests:
        # test[0] is the list with current test scenarios
        # test[1] are the highest moves in the current list with test scenarios
        top_cases = []
        for case in test[0]:
            if case[2] == test[1]:
                top_cases.append(case)

        if top_cases:
            answer.append(top_cases)

    return answer


def test_case(case):
    rows = int(case["height"])
    columns = int(case["width"])
    board = case["board"]
    case_tests = []
    most_moves = 0
    for row in range(0, rows):
        for col in range(0, columns):
            tst = test_starting_point(board, row, col, rows, columns)
            case_tests.append(tst)
            if tst[2] > most_moves:
                most_moves = tst[2]

    return case_tests, most_moves


def test_robot(info):
    results = []
    for case in info["cases"]:
        results.append(test_case(case))

    return format_tests(results)


def main(file):
    info = r_file_and_prep_info(file)
    tests = test_robot(info)
    for scenario in tests:
        if len(scenario) == 1:
            print(*scenario[0])
        else:
            multiple_scenarios = ""
            for single in scenario:
                multiple_scenarios += f"{single[0]} {single[1]} {single[2]};"
            print(multiple_scenarios[:-1])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Input file name: ")

    if not os.path.exists(filename):
        print(f"File '{filename}' not found!")
    else:
        main(filename)
