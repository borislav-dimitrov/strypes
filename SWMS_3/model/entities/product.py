class Product:
    def __init__(self, prod_name: str, prod_type: str, buy_price: float, sell_price: float,
                 quantity: int, assigned_wh, id_: int = None):
        self.id = id_
        self.name = prod_name
        self.type = prod_type
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.quantity = quantity
        self.assigned_wh = assigned_wh
