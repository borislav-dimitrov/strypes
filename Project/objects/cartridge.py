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
