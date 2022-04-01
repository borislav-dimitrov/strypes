from utils.data_utils import to_json_helper


class Warehouse:
    def __init__(self, wh_name: str, wh_type: str, wh_capacity: int, wh_products: list,
                 status: str, id_: int = None):
        self.id = id_
        self.name = wh_name
        self.type = wh_type
        self.capacity = wh_capacity
        self.products = wh_products
        self.status = status

    def to_json(self):
        """Prepare data to be written to json """
        products = to_json_helper(self.products)
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "capacity": self.capacity,
            "products": products,
            "status": self.status
        }
