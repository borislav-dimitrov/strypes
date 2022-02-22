class Warehouse:
    def __init__(self, wh_id, wh_name, wh_type, wh_capacity, wh_status):
        self.wh_id = wh_id
        self.wh_name = wh_name
        self.wh_type = wh_type
        self.wh_capacity = wh_capacity
        self.wh_status = wh_status

    def get_self_info(self):
        info = f"ID: {self.wh_id} | " \
               f"Name: {self.wh_name} | " \
               f"Type: {self.wh_type} | " \
               f"Capacity: {self.wh_capacity} | " \
               f"Status: {self.wh_status} "
        return info
