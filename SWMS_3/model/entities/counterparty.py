class Counterparty:
    def __init__(self, name: str, phone: str, payment_nr: str, status: str, type_: str, descr, id_: int = None):
        """

        :param name:
        :param phone:
        :param payment_nr:
        :param status: "Enabled" or "Disabled"
        :param type_: "Client" or "Supplier"
        :param descr: if type = "Supplier" -> list of info for the products that he can sell, i.e "["material5", "Finished Goods", 10.0, 11.0, None]"
        :param id_:
        """
        self.id = id_
        self.name = name
        self.phone = phone
        self.payment_nr = payment_nr
        self.status = status
        self.type = type_
        self.description = descr
