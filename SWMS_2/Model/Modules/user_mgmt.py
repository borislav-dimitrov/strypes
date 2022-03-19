import sys

import Model.Repositories.users_repo as urep
import Model.DataBase.my_db as db
import json as js


# region Verifications
def verify_user(username, password):
    for user in db.users:
        if user.user_name.lower() == username.lower() and urep.compare_pwd(password, user.user_password):
            return user

    return "Unauthorized"


def verify_password(pwd):
    """
    Check for strong password
    :param pwd: password as string
    :return: True or validation error messages
    """
    status = urep.check_strong_pwd(pwd)
    return status


# endregion


# region CRUD
def create_new_user(id_, name: str, pwd: str, type_: str, stat: str, last_login: str):
    """
    Create new user
    :param id_: New user id or "Auto"
    :param name: Username
    :param pwd: User password
    :param type_: User type
    :param stat: User status
    :param last_login: User last login time
    :return: Status { True / False }
    """

    # region Check if username is free
    if not urep.check_uname_available(name, db.users):
        print("Username already exists!")
        return False
    # endregion

    # region Check strong pwd
    status = verify_password(pwd)
    if status != "":
        print(status)
        return False
    # endregion

    # region Check user type
    if "administrator" in type_.lower():
        utype = "Administrator"
    elif "operator" in type_.lower():
        utype = "Operator"
    else:
        print(f"Invalid user type {type_}!")
        return False
    # endregion

    # region Check user status
    if "enabled" in stat.lower():
        ustat = "ENABLED"
    elif "disabled" in stat.lower():
        ustat = "DISABLED"
    else:
        print(f"Invalid user status {stat}!")
        return False
    # endregion

    # Generate id
    if id_ == "auto":
        id_ = db.get_new_entity_id(db.users)

    # Create new user
    new_usr = urep.create_user(id_, name.lower(), urep.encrypt_pwd(pwd), utype, ustat, last_login)

    # add to db users
    db.users.append(new_usr)
    return True


def delete_user(user_id: int, all_users: list, current_user_logged_in):
    """
    Delete user buy id
    :param user_id: User id
    :param all_users: All current users list
    :param current_user_logged_in: Current user that is login
    :return: None
    """
    status, message = urep.delete_user(user_id, all_users, current_user_logged_in)

    if status:
        db.my_logger.log(__file__, message, "INFO")
        print(status, message)
    if not status:
        db.my_logger.log(__file__, message, "WARNING")
        print(status, message)


def edit_user_name(user_id: int, new_name: str):
    user = urep.get_user_by_id(user_id, db.users)
    if not urep.check_uname_available(new_name, db.users):
        print("Username already exists!")
        return False
    user.user_name = new_name
    save_n_load_users()
    return True


def edit_user_password(user_id: int, new_pwd: str):
    user = urep.get_user_by_id(user_id, db.users)
    status = verify_password(new_pwd)
    if status != "":
        print(status)
        return False
    user.user_password = urep.encrypt_pwd(new_pwd)
    save_n_load_users()
    return True


def edit_user_type(user_id: int, new_type: str):
    user = urep.get_user_by_id(user_id, db.users)
    if "administrator" in new_type.lower():
        utype = "Administrator"
    elif "operator" in new_type.lower():
        utype = "Operator"
    else:
        print(f"Invalid user type {new_type}!")
        return False

    user.user_type = utype
    save_n_load_users()
    return True


def edit_user_status(user_id: int, new_stat: str):
    user = urep.get_user_by_id(user_id, db.users)
    if "enabled" in new_stat.lower():
        ustat = "ENABLED"
    elif "disabled" in new_stat.lower():
        ustat = "DISABLED"
    else:
        print(f"Invalid user status {new_stat}!")
        return False
    user.user_status = ustat
    save_n_load_users()
    return True


def edit_user_last_login(user_id: int, new_last_login: str):
    user = urep.get_user_by_id(user_id, db.users)
    user.last_login = new_last_login
    return True


# endregion


# region Save/Load/Reload
def save_users():
    output_file = "./Model/DataBase/users.json"
    data = {
        "users": []
    }

    for user in db.users:
        data["users"].append({
            "entity_id": user.entity_id,
            "user_name": user.user_name,
            "user_password": user.user_password.decode("utf-8"),
            "user_type": user.user_type,
            "user_status": user.user_status,
            "last_login": user.last_login
        })
    try:
        db.save_data_to_json(data, output_file)
    except Exception as ex:
        msg = "Error saving users!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)


def load_users():
    try:
        with open("./Model/DataBase/users.json", "rt", encoding="utf-8") as file:
            data = js.load(file)
    except Exception as ex:
        msg = "Error reading file!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)

    db.users = []
    try:
        for usr in data["users"]:
            new_usr_id = "auto"
            new_usr_name = usr["user_name"]
            new_usr_pwd = usr["user_password"].encode("utf-8")
            new_usr_type = usr["user_type"]
            new_usr_stat = usr["user_status"]
            new_usr_last_login = usr["last_login"]

            create_new_user(new_usr_id, new_usr_name, urep.decrypt_pwd(new_usr_pwd),
                            new_usr_type, new_usr_stat, new_usr_last_login)
    except Exception as ex:
        msg = "Error Loading users!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)


def save_n_load_users():
    save_users()
    load_users()
# endregion
