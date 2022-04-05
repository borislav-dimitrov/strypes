from model.utils.data_utils import to_json_helper


class Transaction:
    """Class, keeping the information about the Transactions"""

    def __init__(self, type_: str, date: str, counterparty,
                 assets: list, invoice, id_: int = None):
        """
        Initialize new transaction
        :param type_: "Sale" or "Purchase"
        :param date: timestamp of the transaction
        :param counterparty: the counterparty we sold/purchased from/to: Counterparty
        :param assets: products sold in the invoice: TempProduct
        :param invoice: Invoice for the current transaction or None
        :param id_:
        """
        self.id = id_
        self.type = type_
        self.date = date
        self.counterparty = counterparty
        self.assets = assets
        self.price = 0
        self.invoice = invoice

        self._calc_price()

    def _calc_price(self):
        """Calculates the total price based on the transaction products"""
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
