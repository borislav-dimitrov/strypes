class Printer:
    def __init__(self, asset_id, prn_model, cost_centre, location, bk_counters=0,
                 clr_counters=0, status="Active", prn_ip="0.0.0.0", rent=True):
        self.asset_id = asset_id
        self.prn_model = prn_model
        self.cost_centre = cost_centre
        self.location = location
        self.bk_counters = bk_counters
        self.clr_counters = clr_counters
        self.prn_ip = prn_ip
        self.status = status
        self.rent = rent
