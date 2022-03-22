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
        while (row, col) not in passed_through:
            passed_through.append((row, col))

            # Check the direction
            if curr_cell.lower() == "r":
                curr_cell, row, col = move_bot_to(row, col, board, "r")
            elif curr_cell.lower() == "l":
                curr_cell, row, col = move_bot_to(row, col, board, "l")
            elif curr_cell.lower() == "u":
                curr_cell, row, col = move_bot_to(row, col, board, "u")
            elif curr_cell.lower() == "d":
                curr_cell, row, col = move_bot_to(row, col, board, "d")

            if row < 0 or col < 0 or row > rows - 1 or col > columns - 1:
                break

    except IndexError as ex:
        # Robot fell off the table
        return [r + 1, c + 1, len(passed_through) + 1]
    except Exception as ex:
        print("Ooops!", type(ex), ex)
    finally:
        # Robot shutdown
        return [r + 1, c + 1, len(passed_through)]


def format_tests(tests):
    answer = []
    for test in tests:
        highest_moves = 0
        for case in test:
            if case[2] > highest_moves:
                highest_moves = case[2]

        top_cases = []
        for case in test:
            if case[2] == highest_moves:
                top_cases.append(case)

        if top_cases:
            answer.append(top_cases)

    return answer


def test_case(case):
    rows = int(case["height"])
    columns = int(case["width"])
    board = case["board"]
    case_tests = []
    for row in range(0, rows):
        for col in range(0, columns):
            tst = test_starting_point(board, row, col, rows, columns)
            case_tests.append(tst)

    return case_tests


def test_robot(info):
    results = []
    for case in info["cases"]:
        results.append(test_case(case))

    return format_tests(results)


def main():
    info = r_file_and_prep_info("./files/robot.txt")
    answer = test_robot(info)
    for answ in answer:
        if len(answ) == 1:
            print(*answ[0])
        else:
            tmp_answ = ""
            for i in answ:
                tmp_answ += f"{i[0]} {i[1]} {i[2]};"
            print(tmp_answ[:-1])


main()
