class Warehouse:
    def __init__(self, wh_name: str, wh_type: str, wh_capacity: int, wh_products: list,
                 status: str, id_: int = None):
        self.id = id_
        self.name = wh_name
        self.type = wh_type
        self.capacity = wh_capacity
        self.products = wh_products
        self.status = status
