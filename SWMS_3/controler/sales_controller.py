from model.dao.logger import MyLogger
from model.service.modules.sales_module import SalesModule


class SalesController:
    def __init__(self, sales_module: SalesModule, logger: MyLogger):
        self._module = sales_module
        self._logger = logger

    def load_all(self):
        self._module.load_all()

    def save_all(self):
        self._module.save_all()
