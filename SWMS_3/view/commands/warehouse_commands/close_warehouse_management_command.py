class CloseWarehouseMgmtCommand:
    def __init__(self, controller):
        self.controller = controller

    def __call__(self, *args, **kwargs):
        self.controller.close_wh_mgmt()
