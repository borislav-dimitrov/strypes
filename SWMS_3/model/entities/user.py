class User:
    def __init__(self, user_name: str, user_password: str, user_type: str, user_status: str,
                 last_login: str, id_: int = None):
        self.entity_id = id_
        self.user_name = user_name
        self.user_password = user_password
        self.user_type = user_type
        self.user_status = user_status
        self.last_login = last_login
