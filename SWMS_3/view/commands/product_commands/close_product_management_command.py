class CloseProductManagementCommand:
    def __init__(self, controller):
        self.controller = controller

    def __call__(self, *args, **kwargs):
        self.controller.close_product_mgmt()
