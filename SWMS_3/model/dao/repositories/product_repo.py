import sys

from model.dao.repositories.generic_repo import GenericRepository
from model.exceptions import EntityIsAlreadyInWarehouseException


class ProductRepository(GenericRepository):
    def __init__(self, IdGenerator):
        super().__init__(IdGenerator)

    @staticmethod
    def update_assigned_wh(entity, new_wh):
        old_wh = entity.assigned_wh
        try:
            if old_wh is new_wh:
                raise EntityIsAlreadyInWarehouseException(f"Current item '{entity.name}' is already in '{new_wh.name}'")
            # remove item from old wh
            for product in old_wh.products:
                if product is entity:
                    old_wh.products.remove(entity)

            # change product assigned warehouse
            entity.assigned_wh = new_wh

            # add product to the new warehouse
            new_wh.products.append(entity)
        except Exception as ex:
            # TODO log
            tb = sys.exc_info()[2].tb_frame
            print(f"Something went wrong!\nErrType: {type(ex)}\nErr: {ex}\nTraceBack: {tb}")
