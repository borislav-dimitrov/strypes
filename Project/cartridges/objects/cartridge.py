class Cartridge:
    def __init__(self, asset_id, crt_type, serial_number, barcode, cost_centre, date_bought, date_scrap, remark,
                 status="Normal"):
        self.asset_id = asset_id
        self.crt_type = crt_type
        self.serial_number = serial_number
        self.barcode = barcode
        self.cost_centre = cost_centre
        self.date_bought = date_bought
        self.date_scrap = date_scrap
        self.remark = remark
        self.status = status

    def get_all_info(self):
        print(
            f"Cartridge Id: {self.asset_id} | " +
            f"Cartridge Type: {self.crt_type} | " +
            f"Cartridge Serial: {self.serial_number} | " +
            f"Cartridge Barcode: {self.barcode} | " +
            f"Cost Centre Id: {self.cost_centre.asset_id} | " +
            f"Cost Centre Number: {self.cost_centre.number} | " +
            f"Cost Centre Name: {self.cost_centre.name} | " +
            f"Cartridge Date Bought: {self.date_bought} | " +
            f"Cartridge Date Scrap: {self.date_scrap} | " +
            f"Cartridge Remark: {self.remark} | " +
            f"Cartridge Status: {self.status}"
        )
