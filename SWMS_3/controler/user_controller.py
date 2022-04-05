from model.service.logger import MyLogger
from model.service.modules.users_module import UserModule


class UserController:
    def __init__(self, user_module: UserModule, logger: MyLogger):
        self._module = user_module
        self._logger = logger

    def load(self):
        self._module.load()

    def save(self):
        self._module.save()

    def reload(self):
        self.save()
        self.load()
