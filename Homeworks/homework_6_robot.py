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


def move_bot_to(pos, board, direction):
    if direction == "r":
        pos[1] += 1
    if direction == "l":
        pos[1] -= 1
    if direction == "u":
        pos[0] -= 1
    if direction == "d":
        pos[0] += 1
    return board[pos[0]][pos[1]]


def test_starting_point(board, r, c):
    passed_through = []
    steps = 0
    curr_pos = [r, c]
    curr_cell = board[r][c]

    try:
        while tuple(curr_pos) not in passed_through:
            passed_through.append(tuple(curr_pos))

            if curr_cell.lower() == "r" and (curr_pos[0], curr_pos[1] + 1) not in passed_through:
                curr_cell = move_bot_to(curr_pos, board, "r")
            if curr_cell.lower() == "l" and (curr_pos[0], curr_pos[1] - 1) not in passed_through:
                curr_cell = move_bot_to(curr_pos, board, "l")
            if curr_cell.lower() == "u" and (curr_pos[0] + 1, curr_pos[1]) not in passed_through:
                curr_cell = move_bot_to(curr_pos, board, "u")
            if curr_cell.lower() == "d" and (curr_pos[0] - 1, curr_pos[1]) not in passed_through:
                curr_cell = move_bot_to(curr_pos, board, "d")
    except IndexError as ex:
        # Robot fell off the table
        return {"start_row": r + 1, "start_col": c + 1, "total_moves": len(passed_through) + 1}
    except Exception as ex:
        print("Ooops!", type(ex), ex)
    finally:
        # Robot shutdown
        return {"start_row": r + 1, "start_col": c + 1, "total_moves": len(passed_through)}


def filter_tests(tests):
    answers = []
    for i in tests:
        if len(i) > 1:
            tmp = []
            for a in i:
                tmp.append(" ".join(a))
            answers.append(tmp)
            # TODO filter tmp answers
        else:
            answers.append(" ".join(i[0]))
    return answers


def test_case(case):
    rows = int(case["height"])
    columns = int(case["width"])
    board = case["board"]
    case_tests = []
    for row in range(0, rows):
        for col in range(0, columns):
            tst = test_starting_point(board, row, col)
            case_tests.append(tst)

    return case_tests


def test_robot(info):
    results = []
    for case in info["cases"]:
        results.append(test_case(case))

    answer = []
    for res in results:
        tmp_res = []
        for r in res:
            a = r.values()
            r = ", ".join(str(z) for z in a)
            tmp_res.append(r.split(", "))
        answer.append(tmp_res)
    return filter_tests(answer)


def main():
    info = r_file_and_prep_info("./files/robot.txt")
    for result in test_robot(info):
        if isinstance(result, list):
            print(";".join(result))
        else:
            print(result)


main()
