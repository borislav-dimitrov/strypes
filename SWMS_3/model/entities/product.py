class Product:
    def __init__(self, prod_name: str, prod_type: str, buy_price: float, sell_price: float,
                 quantity: int, assigned_wh, id_: int = None):
        self.entity_id = id_
        self.product_name = prod_name
        self.product_type = prod_type
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.quantity = quantity
        self.assigned_wh = assigned_wh
