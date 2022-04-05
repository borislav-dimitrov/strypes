from model.utils.data_utils import to_json_helper


class Warehouse:
    """Class, keeping the information about the Warehouses"""
    def __init__(self, wh_name: str, wh_type: str, wh_capacity: int, wh_products: list,
                 status: str, id_: int = None):
        """
        Initialize Warehouse Object
        :param wh_name:
        :param wh_type: "Finished Goods" or "Raw Materials"
        :param wh_capacity: amount of products that can be stored in: int
        :param wh_products: currently stored Products: Product
        :param status: "Enabled" or "Disabled"
        :param id_:
        """
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
