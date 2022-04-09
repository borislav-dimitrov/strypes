class OpenTransactionMgmtCommand:
    def __init__(self, controller):
        self.controller = controller

    def __call__(self, *args, **kwargs):
        self.controller.transaction_mgmt()
