from Models.Db.fakeDB import login_users
import json


def save_data_to_json(data, file):
    with open(file, "w") as output:
        output.write(json.dumps(data, indent=4))


def save_users():
    output_file = "./Models/Db/loginUsers.json"
    data = {
        "login_users": []
    }
    for user in login_users:
        data["login_users"].append({
            "user_id": user.user_id,
            "user_uname": user.user_name,
            "user_pwd": user.user_pwd.decode("utf-8"),  # we are using decode, so we can store it in the JSON
            "user_type": user.user_type,
            "user_status": user.user_status,
            "user_last_login": user.user_last_login
        })

    save_data_to_json(data, output_file)


def save_all_data():
    save_users()
