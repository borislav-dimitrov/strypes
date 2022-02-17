class User:
    def __init__(self, asset_id, f_name, l_name, cost_centre, status="Active"):
        self.asset_id = asset_id
        self.f_name = f_name
        self.l_name = l_name
        self.cost_centre = cost_centre
        self.status = status
