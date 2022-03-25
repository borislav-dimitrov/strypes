class Transaction:
    def __init__(self, id_, type_, date, price, counterparty, assets, invoice):
        self.entity_id = id_
        self.type_ = type_
        self.date = date
        self.price = price
        self.counterparty = counterparty
        self.assets = assets
        self.invoice = invoice
