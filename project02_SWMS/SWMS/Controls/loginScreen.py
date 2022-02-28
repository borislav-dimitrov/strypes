from Models.Db.fakeDB import login_users
from Services.userServices import *


def user_is_valid(uname, pwd):
    for user in login_users:
        if user.user_name.lower() == uname.lower() and compare_pwd(pwd, user.user_pwd):
            return user

    return False

