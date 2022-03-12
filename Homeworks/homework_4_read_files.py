import re
from os.path import exists


def get_count_by_word(look_for: str, list_: list[tuple]) -> int:
    """
    Search for how many times the word has been found in the file
    :param look_for: Word
    :param list_: List to look in
    :return: Times found in the file
    """
    for item in list_:
        if look_for == item[0]:
            return item[1]
    return 0


def merge_words(words_1: list[tuple], words_2: list[tuple]) -> list:
    """
    Merge two word lists
    :param words_1: List with matched words and times used
    :param words_2: List with matched words and times used
    :return: Merged list
    """
    merged = []
    words_only_1 = [i[0] for i in words_1]
    words_only_2 = [i[0] for i in words_2]
    all_words = []

    for word in words_1:
        if word[0] not in all_words:
            all_words.append(word[0])
    for word in words_2:
        if word[0] not in all_words:
            all_words.append(word[0])

    # Match words
    for word in all_words:
        # For file 1
        current_row = [word]
        if word in words_only_1:
            times_found1 = get_count_by_word(word, words_1)
            current_row.append(times_found1)
        else:
            current_row.append(0)
        if word in words_only_2:
            times_found2 = get_count_by_word(word, words_2)
            current_row.append(times_found2)
        else:
            current_row.append(0)
        merged.append(current_row)

    return merged


def read_file(file: str, filter_pattern: str = r'\W+'):
    """
    Filter given file and return key words + count
    :param file: File name if in same dir. If not full path
    :param filter_pattern: Regex filter pattern
    :return: list with matched keywords and times used
    """
    all_words = {}
    with open(file, mode="rt", encoding="utf-8") as f:
        for line in f:
            # Remove the commentaries
            words = line.strip().split("#")[0]
            # Add the desired filter pattern
            words = re.split(filter_pattern, words.strip())
            for word in words:
                if word != "":
                    all_words[word] = all_words.get(word, 0) + 1

    # Sort descending
    work_items: list[tuple[str, int]] = list(all_words.items())
    work_items.sort(key=lambda t: t[1], reverse=True)
    return work_items


def calc_difference(list_: list[tuple]) -> float:
    """
    Calculate the difference between the two files
    :param list_: List with tuples ( word, times in file-1, times in file-2 )
    :return: int
    """
    N = len(list_)
    total = 0
    for item in list_:
        current = item[1] - item[2]
        if current < 0:
            current *= -1
        total += current
    print(f"N = i = {N}\n")
    return round(float(total / N), 20)


if __name__ == '__main__':
    file1 = input("Input file1 name: ")
    file2 = input("Input file2 name: ")
    if not exists(file1):
        print(f"File \"{file1}\" not found!")
        quit()

    if not exists(file2):
        print(f"File \"{file2}\" not found!")
        quit()

    file_1_words = read_file(file1)
    print("\nWords from file1\n", file_1_words, "\n")
    file_2_words = read_file(file2)
    print("Words from file2\n", file_2_words, "\n")

    merged = merge_words(file_1_words, file_2_words)
    print("List with mapped words from both files\n", merged, "\n")

    difference = calc_difference(merged)
    print(f"Степен на различност = {difference}")
