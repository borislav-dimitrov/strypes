class Transaction:
    def __init__(self, type_: str, date: str, counterparty,
                 assets: list, invoice, id_: int = None):
        self.id = id_
        self.type_ = type_
        self.date = date
        self.counterparty = counterparty
        self.assets = assets
        self.price = 0
        self.invoice = invoice

        self.calc_price()

    def calc_price(self):
        # Calc price
        for temp_product in self.assets:
            # price = price * amount to sell/buy
            self.price += round(float(temp_product.price * temp_product.quantity), 2)
