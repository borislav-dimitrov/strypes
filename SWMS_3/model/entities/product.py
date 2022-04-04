from utils.data_utils import to_json_helper


class Product:
    """Class, keeping the information about the Products"""
    def __init__(self, prod_name: str, prod_type: str, buy_price: float, sell_price: float,
                 quantity: int, assigned_wh, id_: int = None):
        """
        Initialize Product object
        :param prod_name:
        :param prod_type: "Raw Materials" or "Finished Goods"
        :param buy_price:
        :param sell_price:
        :param quantity: amount of the same product
        :param assigned_wh: assigned warehouse: Warehouse
        :param id_:
        """
        self.id = id_
        self.name = prod_name
        self.type = prod_type
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.quantity = quantity
        self.assigned_wh = assigned_wh

    def to_json(self):
        """Prepare data to be written to json """
        wh = self.assigned_wh
        conditions = [isinstance(wh, list), isinstance(wh, tuple), isinstance(wh, dict),
                      isinstance(wh, str), isinstance(wh, int), wh is None]
        if not any(conditions):
            wh = {"id": self.assigned_wh.id, "name": self.assigned_wh.name}

        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "buy_price": self.buy_price,
            "sell_price": self.sell_price,
            "quantity": self.quantity,
            "assigned_wh": wh
        }
