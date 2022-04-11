class GenWhProductsTreeViewCommand:
    def __init__(self, controller, view):
        self.controller = controller
        self.view = view

    def __call__(self, *args, **kwargs):
        self.controller.refresh_products_treeview_vars(self.view)
