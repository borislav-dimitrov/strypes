import json
import Services.tkinterServices as Tkserv


def load_users():
    file = open("./Models/Db/loginUsers.json")
    data = ""
    try:
        data = json.load(file)
    except Exception as ex:
        if "Expecting value" in str(ex):
            data = ""

    all_info = []
    # if users file is empty create form for a new system user
    # else load all the users
    if data == "" or len(data["login_users"])<1:
        tmp_user = Tkserv.create_system_user()
        all_info.append(tmp_user)
    else:
        for line in data["login_users"]:
            all_info.append(line)
    return all_info
