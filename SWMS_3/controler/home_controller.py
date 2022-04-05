from model.entities.user import User
from model.service.logger import MyLogger


class HomeController:
    def __init__(self, logger: MyLogger):
        self._logger = logger
        self._logged_user: User = None
        self._logging_out = False

    @staticmethod
    def test():
        print("test")
