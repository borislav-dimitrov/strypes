from Models.Data.loadData import load_users
from Models.Assets.user import User
from Services.userServices import check_user_before_create

login_users = []
curr_user = None


def create_users(data):
    for user in data:
        # check if user already exist
        user_available = check_user_before_create(login_users, user["user_id"], user["user_uname"])
        if user_available is True:
            # add user
            new_user = User(user["user_id"],
                            user["user_uname"],
                            user["user_pwd"].encode("utf-8"),  # encoding because it comes as a string from the json
                            user["user_type"],
                            user["user_status"],
                            user["user_last_login"], )
            login_users.append(new_user)
        else:
            return user_available
    return "Success"


def load_and_create_users():
    # clear objects before loading
    login_users.clear()
    # load the new objects
    try:
        users_from_file = load_users()
        status = create_users(users_from_file)
        return status
    except TypeError as ex:
        return "Fail! Couldn't create user!"
