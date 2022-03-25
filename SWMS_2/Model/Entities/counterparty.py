class Counterparty:
    def __init__(self, entity_id, name, phone, payment_nr, status, type_, descr):
        self.entity_id = entity_id
        self.name = name
        self.phone = phone
        self.payment_nr = payment_nr
        self.status = status
        self.type_ = type_
        self.description = descr
