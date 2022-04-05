from model.service.logger import MyLogger
from model.service.modules.warehousing_module import WarehousingModule


class WarehousingController:
    def __init__(self, warehousing_module: WarehousingModule, logger: MyLogger):
        self._module = warehousing_module
        self._logger = logger

    def load_all(self):
        self._module.load_all()

    def save_all(self):
        self._module.save_all()

    def reload(self):
        self.save_all()
        self.load_all()
