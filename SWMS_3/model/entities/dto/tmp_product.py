class TempProduct:
    """
    TempProduct class, used to link the products between the transactions and invoices
    """
    def __init__(self, name: str, type_: str, price: float, quantity: int):
        self.name = name
        self.type_ = type_
        self.price = price
        self.quantity = quantity

    def to_json(self):
        """Prepare data to be written to json """
        return {
            "name": self.name,
            "type": self.type_,
            "price": self.price,
            "quantity": self.quantity
        }
