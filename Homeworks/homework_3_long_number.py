import random
from datetime import datetime


def long_number(n, a, f):
    """
    Largest n = 200000 { 2*10^5 }
    :param n: given number length { }
    :param a: given number { int }
    :param f: mapping function
    :return: int
    """
    new_f_func = str()
    a_to_list = [str(i) for i in str(a)]

    # Remove intervals from f if any
    for item in f:
        if item.isnumeric():
            new_f_func += str(item)

    # Changes map f to a
    for item in range(1, n + 1):
        index = item - 1
        current_number = a_to_list[index]

        if int(current_number) <= int(new_f_func[int(current_number) - 1]):
            a_to_list[index] = new_f_func[int(current_number) - 1]

        item += 1

    return ''.join(a_to_list)


def main():
    digits = 2 * (pow(10, 5))
    number = str()
    for i in range(1, digits + 1):
        number += str(random.randint(1, 9))

    number = number
    f_func = "1 2 5 4 6 6 3 1 9"
    try:
        answer = long_number(digits, number, f_func)
        if int(answer) >= int(number):
            return True
        else:
            return False
    except Exception as ex:
        return ex


if __name__ == '__main__':
    attempt = 1
    for i in range(0, 10):
        now = datetime.now()
        start_time = now.strftime("%H:%M:%S")
        status = main()
        now = datetime.now()
        finish_time = now.strftime("%H:%M:%S")
        print(f"Attempt: {attempt}    -    {status}    -    Started: {start_time}    -    Finished: {finish_time}")

        attempt += 1
