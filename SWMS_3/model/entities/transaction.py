from utils.data_utils import to_json_helper


class Transaction:
    def __init__(self, type_: str, date: str, counterparty,
                 assets: list, invoice, id_: int = None):
        self.id = id_
        self.type = type_
        self.date = date
        self.counterparty = counterparty
        self.assets = assets
        self.price = 0
        self.invoice = invoice

        self.calc_price()

    def calc_price(self):
        # Calc price
        for product in self.assets:
            self.price += round(float(product.price * product.quantity), 2)

    def to_json(self):
        """Prepare data to be written to json """
        cpty = to_json_helper(self.counterparty)
        assets = to_json_helper(self.assets)
        inv = to_json_helper(self.invoice)
        return {
            "id": self.id,
            "type": self.type,
            "date": self.date,
            "counterparty": cpty,
            "assets": assets,
            "price": self.price,
            "invoice": inv
        }
