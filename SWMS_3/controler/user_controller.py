from model.service.logger import MyLogger
from model.service.modules.users_module import UserModule


class UserController:
    def __init__(self, user_module: UserModule, logger: MyLogger):
        self._module = user_module
        self._logger = logger

    def login(self, username, password):
        user = self._module.find_by_attribute("name", username.lower())
        if user is not None:
            valid_pwd = self._module._pwd_mgr.compare(password, user[0].password)
            if valid_pwd:
                return True, "Login successful!", user[0]
            else:
                return False, "Wrong password!", None
        return False, "User not found!", None

    def load(self):
        self._module.load()

    def save(self):
        self._module.save()

    def reload(self):
        self.save()
        self.load()
