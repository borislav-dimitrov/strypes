class User:
    def __init__(self, user_name: str, user_password: str, user_type: str, status: str,
                 last_login: str = "", id_: int = None):
        self.id = id_
        self.name = user_name
        self.password = user_password
        self.type = user_type
        self.status = status
        self.last_login = last_login

    def to_json(self):
        return vars(self)
