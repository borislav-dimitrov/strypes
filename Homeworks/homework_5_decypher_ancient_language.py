import sys


def read_file(file):
    with open(file, "rt", encoding="utf-8") as f:
        lines = f.readlines()

    var = lines[0].strip()
    info = []

    for line in range(1, len(lines)):
        info.append(lines[line].strip())

    return var, info


def test_string(curr_str, word_to_match):
    """
    Receive a word to test and the word from our file.
    Convert them to unicode symbols, so we can recognise lower and upper cases
    Sort the converted words and check if they are equal
    :param curr_str: The string we want to test
    :param word_to_match: The word we got from the file
    :return: status { True or False } , tested string or -1
    """
    curr_uni = sorted(curr_str.encode())
    word_uni = sorted(word_to_match.encode())
    if curr_uni == word_uni:
        return True, curr_str
    else:
        return False, -1


def add_percents_and_sort(words, total_words):
    """
    Receive Dictionary with words and total count of words found
    Calculate the percentages for each word
    Create new Dictionary with all the info and sort it by times found
    :param words: Dictionary with words
    :param total_words: Total count of words found
    :return: Sorted Dictionary by times found
    """
    new_words = {}
    words: list[tuple[str, int]] = list(words.items())
    words.sort(key=lambda t: t[1], reverse=True)
    for word in words:
        new_words[word[0]] = [word[1], f"{round(((word[1] / total_words) * 100), 2)}%"]
    return new_words


def top_words(words):
    """
    List with all the words we found in the text
    Count them
    Calculate percentage for each word found
    Create dictionary with the new data and sort it by times found
    :param words: Receive list with words
    :return: Dictionary sorted by times found
    """
    total_words = len(words)
    sorted_words = sorted(words)
    words_dict = {}
    times_met = 1

    for word in range(0, len(sorted_words)):
        current_word = sorted_words[word]
        if word == 0:
            words_dict[current_word] = times_met
            times_met += 1
        else:
            prev_word = sorted_words[word - 1]
            if current_word == prev_word:
                words_dict[current_word] = times_met
                times_met += 1
            else:
                times_met = 1
                words_dict[current_word] = times_met
                times_met += 1

        word += 1

    words_dict = add_percents_and_sort(words_dict, total_words)
    return words_dict


def main():
    # Take filename from parameters or from input
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Input file name: ")
    W, T = read_file(filename)
    T = "".join(T)
    max_W_length = 300
    max_T_length = 3000000
    W_length = len(W) - 1
    T_length = len(T) - 1

    # Validate the variables that we read from file
    if W_length < 1 or W_length > max_W_length:
        print(f"Думата 'W' трябва да е с дължина от 1 до {max_W_length} символа.")
        return

    if T_length < 1 or T_length > max_T_length:
        print(f"Съдържанието 'T' трябва да е с дължина от 1 до {max_T_length} символа.")
        return

    curr_pos = 0
    words_found = []

    # We get every W length words and match them against W until the text T is over
    while curr_pos <= T_length - W_length:
        if curr_pos == 0:
            status, word = test_string(T[curr_pos: W_length + 1], W)
        else:
            status, word = test_string(T[curr_pos: (W_length + 1) + curr_pos], W)

        if status:
            words_found.append(word)

        curr_pos += 1

    # Pass the words found for further formatting
    final_dict = top_words(words_found)

    print(f"Намерени думи -> {len(words_found)}")
    # Print top n words
    first_n_words = 20
    counter = 0
    for word in final_dict:
        if counter >= first_n_words:
            break
        print(word, final_dict[word])
        counter += 1


main()
