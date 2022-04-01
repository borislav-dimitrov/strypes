from utils.data_utils import to_json_helper


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

    def to_json(self):
        """Prepare data to be written to json """
        descr = to_json_helper(self.description)
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "payment_nr": self.payment_nr,
            "status": self.status,
            "type": self.type,
            "description": descr
        }
