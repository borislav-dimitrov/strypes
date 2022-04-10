class RemFromCartCommand:
    def __init__(self, controller):
        self.controller = controller

    def __call__(self, *args, **kwargs):
        self.controller.pur_rem_from_cart()
