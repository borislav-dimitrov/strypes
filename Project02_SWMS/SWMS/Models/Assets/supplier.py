class Supplier:
    def __init__(self, supp_id, supp_name, supp_phone, supp_iban, supp_status):
        self.supp_id = supp_id
        self.supp_name = supp_name
        self.supp_phone = supp_phone
        self.supp_iban = supp_iban
        self.supp_status = supp_status

    def get_self_info(self):
        info = f"ID: {self.supp_id} | " \
               f"Name: {self.supp_name} | " \
               f"Phone: {self.supp_phone} | " \
               f"IBAN: {self.supp_iban} | " \
               f"Status: {self.supp_status} "
        return info