class User:
    def __init__(self, user_name: str, user_password: str, user_type: str, status: str,
                 last_login: str = "", id_: int = None):
        self.id = id_
        self.name = user_name.lower()
        self.password = user_password
        self.type = user_type
        self.status = status
        self.last_login = last_login

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password.decode(),
            "type": self.type,
            "status": self.status,
            "last_login": self.last_login
        }
