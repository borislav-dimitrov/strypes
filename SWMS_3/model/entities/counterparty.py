class Counterparty:
    def __init__(self, name: str, phone: str, payment_nr: str, status: str, type_: str, descr: str, id_: int = None):
        self.id = id_
        self.name = name
        self.phone = phone
        self.payment_nr = payment_nr
        self.status = status
        self.type_ = type_
        self.description = descr
