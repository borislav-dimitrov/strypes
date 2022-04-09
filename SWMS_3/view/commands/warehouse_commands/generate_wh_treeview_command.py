class GenWhTreeViewCommand:
    def __init__(self, controller):
        self.controller = controller

    def __call__(self, *args, **kwargs):
        self.controller.generate_treeview_for_wh()
