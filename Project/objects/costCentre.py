class CostCentre:
    def __init__(self, asset_id, number, name, status="Active"):
        self.asset_id = asset_id
        self.number = number
        self.name = name
        self.status = status

    def get_all_info(self):
        print(
            f"Cost Centre Id: {self.asset_id} | " +
            f"Cost Centre Number: {self.number} | " +
            f"Cost Centre Name: {self.name} | " +
            f"Cost Centre Status: {self.status}"
        )
