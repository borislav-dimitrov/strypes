class Transaction:
    def __init__(self, type_: str, date: str, price: float, counterparty,
                 assets: list, invoice, id_: int = None):
        self.id = id_
        self.type_ = type_
        self.date = date
        self.price = price
        self.counterparty = counterparty
        self.assets = assets
        self.invoice = invoice
