class GetClientsTreeViewCommand:
    def __init__(self, controller):
        self.controller = controller

    def __call__(self, *args, **kwargs):
        self.controller.find_clients_for_treeview()
