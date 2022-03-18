class Product:
    def __init__(self, entity_id, prod_name, prod_type, buy_price, sell_price, quantity, assigned_wh):
        self.entity_id = entity_id
        self.product_name = prod_name
        self.product_type = prod_type
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.quantity = quantity
        self.assigned_wh = assigned_wh
