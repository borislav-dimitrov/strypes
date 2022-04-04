class User:
    """Class, keeping the information about the Users"""
    def __init__(self, user_name: str, user_password: str, user_type: str, status: str,
                 last_login: str = "", id_: int = None):
        """
        Initialize User Object
        :param user_name:
        :param user_password:
        :param user_type: "Administrator" or "Operator"
        :param status: "Enabled" or "Disabled"
        :param last_login: timestamp
        :param id_:
        """
        self.id = id_
        self.name = user_name.lower()
        self.password = user_password
        self.type = user_type
        self.status = status
        self.last_login = last_login

    def to_json(self):
        """Prepare data to be written to json """
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password.decode(),
            "type": self.type,
            "status": self.status,
            "last_login": self.last_login
        }
