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

    def get_all_info(self):
        print(
            f"Printer Id: {self.asset_id} | " +
            f"Printer Model: {self.prn_model} | " +
            f"Cost Centre Id: {self.cost_centre.asset_id} | " +
            f"Cost Centre Number: {self.cost_centre.number} | " +
            f"Cost Centre Name: {self.cost_centre.name} | " +
            f"Printer Location: {self.location} | " +
            f"Printer Black Counters: {self.bk_counters} | " +
            f"Printer Color Counters: {self.clr_counters} | " +
            f"Printer Status: {self.status} | " +
            f"Printer Rent: {self.rent}"
        )
