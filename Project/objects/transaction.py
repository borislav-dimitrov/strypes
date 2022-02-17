class Transaction:
    def __init__(self, asset_id, cartridge, user, cost_centre, delivery_date,
                 service_date, from_service_date, return_to_user_date, status="Waiting for service"):
        self.asset_id = asset_id
        self.cartridge = cartridge
        self.user = user
        self.cost_centre = cost_centre
        self.delivery_date = delivery_date
        self.service_date = service_date
        self.from_service_date = from_service_date
        self.return_to_user_date = return_to_user_date
        self.status = status

    def get_all_info(self):
        print(
            f"Transaction Id: {self.asset_id} | " +
            f"Cartridge Id: {self.cartridge.asset_id} | " +
            f"Cartridge Type: {self.cartridge.crt_type} | " +
            f"User Id: {self.user.asset_id} | " +
            f"User Name: {self.user.f_name} {self.user.l_name} | " +
            f"Bill is going to: {self.cost_centre.asset_id} | {self.cost_centre.number} | {self.cost_centre.name}" +
            f"Delivered by user on: {self.delivery_date} | " +
            f"Gave to service on: {self.service_date} | " +
            f"Received from service on: {self.from_service_date} | " +
            f"Returned to user on: {self.return_to_user_date} | " +
            f"User Status: {self.status}"
        )
