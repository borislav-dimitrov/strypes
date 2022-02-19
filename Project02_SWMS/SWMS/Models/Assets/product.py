class Product:
    def __init__(self, product_id, product_name, product_type, buy_price, sell_price):
        self.product_id = product_id
        self.product_name = product_name
        self.product_type = product_type
        self.buy_price = buy_price
        self.sell_price = sell_price

    def get_self_info(self):
        info = f"ID: {self.product_id} | " \
               f"Name: {self.product_name} | " \
               f"Type: {self.product_type} | " \
               f"Buy Price: {self.buy_price} | " \
               f"Sell Price: {self.sell_price}"
        return info
