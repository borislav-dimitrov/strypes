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
