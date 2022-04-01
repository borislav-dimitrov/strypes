class WarehousingModule:
    def __init__(self, product_repository, warehouse_repository):
        self._products = product_repository
        self._warehouses = warehouse_repository
