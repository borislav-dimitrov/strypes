import sys

from model.dao.repositories.generic_repo import GenericRepository
from model.exceptions import EntityIsAlreadyInWarehouseException


class WarehouseRepository(GenericRepository):
    def __init__(self, IdGenerator):
        super().__init__(IdGenerator)

    @staticmethod
    def add_warehouse_products(warehouse, products: list):
        try:
            for product in products:
                old_wh = product.assigned_wh

                if old_wh is not None and old_wh is not warehouse:
                    # remove from old warehouse
                    for entity in old_wh.products:
                        if entity is product:
                            old_wh.products.remove(entity)

                    # change product wh
                    product.assigned_wh = warehouse

                    # add to new
                    warehouse.products.append(product)
                else:
                    raise EntityIsAlreadyInWarehouseException(
                        f"Product '{product.name}' is already in warehouse '{warehouse.name}'!")
        except Exception as ex:
            # TODO log
            tb = sys.exc_info()[2].tb_frame
            print(f"Something went wrong!\nErrType: {type(ex)}\nErr: {ex}\nTraceBack: {tb}")

    def delete_by_id(self, id_):
        try:
            old = self.find_by_id(id_)

            # remove products assigned warehouse
            for product in old.products:
                product.assigned_wh = None

            # delete warehouse
            del self._entities[id_]
            return old
        except Exception as ex:
            # TODO log
            tb = sys.exc_info()[2].tb_frame
            print(f"Something went wrong!\nErrType: {type(ex)}\nErr: {ex}\nTraceBack: {tb}")

    def find_by_product(self, product):
        try:
            result = []
            for entity in self._entities:
                if product in self._entities[entity].products:
                    result.append(self._entities[entity])

            if len(result) > 0:
                return result
            else:
                return None
        except Exception as ex:
            # TODO log
            tb = sys.exc_info()[2].tb_frame
            print(f"Something went wrong!\nErrType: {type(ex)}\nErr: {ex}\nTraceBack: {tb}")
