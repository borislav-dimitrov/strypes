class User:
    def __init__(self, user_id, user_name, user_pwd, user_type, user_status, user_last_login):
        self.user_id = user_id
        self.user_name = user_name
        self.user_pwd = user_pwd
        self.user_type = user_type
        self.user_status = user_status
        self.user_last_login = user_last_login

    def get_self_info(self):
        info = f"ID: {self.user_id} | " \
               f"Name: {self.user_name} | " \
               f"Type: {self.user_type} | " \
               f"Status: {self.user_status} | " \
               f"Last Login: {self.user_last_login}"
        return info