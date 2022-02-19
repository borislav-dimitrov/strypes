class User:
    def __init__(self, asset_id, f_name, l_name, cost_centre, status="Active"):
        self.asset_id = asset_id
        self.f_name = f_name
        self.l_name = l_name
        self.cost_centre = cost_centre
        self.status = status

    def get_all_info(self):
        print(
            f"User Id: {self.asset_id} | " +
            f"User First Name: {self.f_name} | " +
            f"User Last Name: {self.l_name} | " +
            f"Cost Centre Id: {self.cost_centre.asset_id} | " +
            f"Cost Centre Number: {self.cost_centre.number} | " +
            f"Cost Centre Name: {self.cost_centre.name} | " +
            f"User Status: {self.status}"
        )
