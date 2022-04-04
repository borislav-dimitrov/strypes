from model.dao.logger import MyLogger
from model.entities.warehouse import Warehouse
from model.service.modules.warehousing_module import WarehousingModule


class WarehousingController:
    def __init__(self, warehousing_module: WarehousingModule, logger: MyLogger):
        self._module = warehousing_module
        self._logger = logger

    def find_warehouse_by_id(self, id_):
        return self._module.find_wh_by_id(id_)

    def create_product(self, name: str, type_: str, b_price: float, s_price: float, qty: int, wh: Warehouse):
        return self._module.create_product(name, type_, b_price, s_price, qty, wh)

    def load_all(self):
        self._module.load_all()

    def save_all(self):
        self._module.save_all()

    def print_all(self):
        self._module.print_all_products()
        print()
        self._module.print_all_wh()
