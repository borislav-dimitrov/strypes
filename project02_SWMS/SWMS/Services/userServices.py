from cryptography.fernet import Fernet
from config import *


def check_user_before_create(all_users, curr_user_id, curr_user_name):
    for user in all_users:
        if curr_user_id == user.user_id:
            return f"User with id: {curr_user_id}\nalready exists!"
        if curr_user_name.lower() == user.user_name.lower():
            return f"User with name: {curr_user_name}\nalready exists!"

    return True


def encrypt_pwd(plain):
    cipher_suite = Fernet(KEY)
    encoded_pwd = cipher_suite.encrypt(f"{plain}".encode())
    return encoded_pwd


def decrypt_pwd(encrypted):
    cipher_suite = Fernet(KEY)
    return cipher_suite.decrypt(encrypted).decode()


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


def get_user_index_by_id(user_id, all_users):
    for user in range(len(all_users)):
        if all_users[user].user_id == int(user_id):
            return user

    return None


def get_user_type_by_id(user_id, all_users):
    for user in all_users:
        if user.user_id == int(user_id):
            return user.user_type
