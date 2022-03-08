# import random
# from datetime import datetime


def long_number(n: int, a: str, f: str) -> int:
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

    # Map f to a
    for item in range(1, n + 1):
        index = item - 1
        current_number = a_to_list[index]

        if int(current_number) <= int(new_f_func[int(current_number) - 1]):
            a_to_list[index] = new_f_func[int(current_number) - 1]

        item += 1

    return int(''.join(a_to_list))


# Test functionality
# def test(number_length: int, func: str):
#     """
#     Test functionality
#     :param number_length: Number length
#     :param func: Mapping function
#     :return: Test status { Bool } or { Exception }
#     """
#     digits = number_length
#     number = str()
#     for i in range(1, digits + 1):
#         number += str(random.randint(1, 9))
#
#     number = number
#     func = func
#     try:
#         answer = long_number(digits, number, func)
#         if answer >= int(number):
#             return True
#         else:
#             return False
#     except Exception as ex:
#         return ex


if __name__ == '__main__':
    digits = int(input("Number length: "))
    number = input("Number: ")
    f_func = input("Number length: ")
    print(long_number(digits, number, f_func))

    # Test functionality
    """
    attempt = 1
    total_attempts = 20
    for i in range(0, total_attempts):
        now = datetime.now()
        start_time = now.strftime("%H:%M:%S")
        status = test(2 * (pow(10, 5)), "1 2 5 4 6 6 3 1 9")
        now = datetime.now()
        finish_time = now.strftime("%H:%M:%S")
        print(f"Attempt: {attempt}    -    {status}    -    Started: {start_time}    -    Finished: {finish_time}")

        attempt += 1
    """
