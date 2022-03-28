class Warehouse:
    def __init__(self, wh_name: str, wh_type: str, wh_capacity: int, wh_products: list,
                 wh_status: str, id_: int = None):
        self.entity_id = id_
        self.wh_name = wh_name
        self.wh_type = wh_type
        self.wh_capacity = wh_capacity
        self.wh_products = wh_products
        self.wh_status = wh_status
