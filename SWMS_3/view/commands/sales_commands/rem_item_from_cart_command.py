class RemItemFromCartCommand:
    def __init__(self, controller):
        self.controller = controller

    def __call__(self, *args, **kwargs):
        self.controller.sell_rem_item_from_cart()
