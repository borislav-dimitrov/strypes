from cryptography.fernet import Fernet
from Model.Entities.user import User
import Resources.config as cfg


# region Checks
def check_uname_available(username, all_users):
    for user in all_users:
        if user.user_name.lower() == username.lower():
            return False
    return True


def check_strong_pwd(pwd: str) -> str:
    """
    Validate password
    :param pwd: password
    :return: Status
    """
    specials = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "[", "{", "]", "}", ";", ":",
                "'", "\"", "\\", "|", ",", "<", ".", ">", "/", "?", "`", "~"]
    validations = ""
    if len(pwd) < 8:
        validations += "Password must be at least 8 characters long!\n"
    if not any(char.isupper() for char in pwd):
        validations += "Password should have at least one uppercase letter!\n"
    if not any(char.islower() for char in pwd):
        validations += "Password should have at least one lowercase letter!\n"
    if not any(char in specials for char in pwd):
        validations += "Password should contain at least one special character!"

    if validations == "":
        return ""
    else:
        return validations


# endregion

# region CRUD
def create_user(id_, name, pwd, type_, status, last_login):
    new_user = User(id_, name, pwd, type_, status, last_login)
    return new_user


def edit_user():
    pass


def delete_user(user_id: int, all_users: list[User], current_user_logged_in: User) -> tuple[bool, str]:
    """
    Delete user buy id
    :param user_id: User id
    :param all_users: All current users list
    :param current_user_logged_in: Current user that is login
    :return: Bool, Message
    """
    for user in all_users:
        if user.entity_id == user_id:
            if user == current_user_logged_in:
                return False, f"Cannot delete currently logged in user!"
            deleted_user_name = user.user_name
            index = get_user_index(user_id, all_users)
            all_users.pop(index)
            return True, f"User {deleted_user_name} deleted successfully!"
    return False, f"User with id of {user_id} not found!"


# endregion

# region Password
def encrypt_pwd(plain):
    cipher_suite = Fernet(cfg.KEY)
    encoded_pwd = cipher_suite.encrypt(f"{plain}".encode())
    return encoded_pwd


def decrypt_pwd(encrypted):
    cipher_suite = Fernet(cfg.KEY)
    return cipher_suite.decrypt(encrypted).decode()


def compare_pwd(plain, encrypted):
    cipher_suite = Fernet(cfg.KEY)
    decoded = cipher_suite.decrypt(encrypted).decode()
    if plain == decoded:
        return True
    else:
        return False


# endregion

# region get objects
def get_user_by_id(user_id: int, all_users: list[User]):
    """
    Get user object buy its id
    :param user_id: User id as int
    :param all_users: All current users
    :return: User object / None
    """
    for user in all_users:
        if user.entity_id == user_id:
            return user
    return None


def get_user_index(user_id, all_users):
    for user in all_users:
        if user.user_id == user_id:
            return all_users.index(user)
    return None
# endregion
