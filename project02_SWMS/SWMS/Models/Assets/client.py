class Client:
    def __init__(self, client_id, client_name, client_phone, client_iban, client_status):
        self.client_id = client_id
        self.client_name = client_name
        self.client_phone = client_phone
        self.client_iban = client_iban
        self.client_status = client_status

    def get_self_info(self):
        info = f"ID: {self.client_id} | " \
               f"Name: {self.client_name} | " \
               f"Phone: {self.client_phone} | " \
               f"IBAN: {self.client_iban} | " \
               f"Status: {self.client_status} "
        return info