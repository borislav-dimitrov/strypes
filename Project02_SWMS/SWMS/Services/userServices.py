from cryptography.fernet import Fernet
from config import *


def check_user_before_create(all_users, curr_user_id, curr_user_name):
    for user in all_users:
        if curr_user_id == user.user_id:
            return f"There was a conflict!\nUser with id: {curr_user_id}\nalready exists!"
        if curr_user_name == user.user_name:
            return f"There was a conflict!\nUser with name: {curr_user_name}\nalready exists!"

    return True


def encrypt_pwd(plain):
    cipher_suite = Fernet(KEY)
    encoded_pwd = cipher_suite.encrypt(f"{plain}".encode())
    return encoded_pwd


def compare_pwd(plain, encrypted):
    cipher_suite = Fernet(KEY)
    decoded = cipher_suite.decrypt(encrypted).decode()
    if plain == decoded:
        return True
    else:
        return False


def get_user_by_id(user_id, all_users):
    for user in all_users:
        if user.user_id == int(user_id):
            return user
    return None


def get_id_for_new_user(all_users):
    highest_id = 0
    for user in all_users:
        if user.user_id + 1 > highest_id:
            highest_id = user.user_id

    return highest_id + 1
