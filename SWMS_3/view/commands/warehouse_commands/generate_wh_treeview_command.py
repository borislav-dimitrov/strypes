class GenWhProductsTreeViewCommand:
    def __init__(self, controller, view):
        self.controller = controller
        self.view = view

    def __call__(self, *args, **kwargs):
        self.controller.generate_treeview_for_wh_products(self.view)
