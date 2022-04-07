from tkinter import ttk

from view.base_view import BaseView
from view.components.item_list import ItemList

# Commands
from view.commands.product_commands.close_product_management_command import CloseProductManagementCommand
from view.commands.product_commands.del_product_command import DelProductCommand
from view.commands.product_commands.show_create_product_command import ShowCreateProductCommand
from view.commands.product_commands.show_edit_product_command import ShowEditProductCommand


class ProductManagementView(BaseView):
    def __init__(self, parent, page_name, controller, open_views, resolution: tuple = (1280, 728),
                 grid_rows=30, grid_cols=30, icon=None):
        super().__init__(parent, page_name, resolution, grid_rows, grid_cols, icon)
        self.parent = parent
        self.controller = controller
        self.open_views = open_views

        # Products dropdown
        self.products_var = self.controller.products
        self.item_list = ItemList(self.parent, self.products_var, 7, 2, colspan=self.cols - 5)

        # Create Button
        self.create_btn = ttk.Button(self.parent, text="Create Product", command=ShowCreateProductCommand(self.controller))
        self.create_btn.grid(row=20, column=5, columnspan=3, sticky="nsew")

        # Update Button
        self.edit_btn = ttk.Button(self.parent, text="Update Product", command=ShowEditProductCommand(self.controller))
        self.edit_btn.grid(row=20, column=14, columnspan=3, sticky="nsew")

        # Delete Button
        self.del_btn = ttk.Button(self.parent, text="Delete Product", command=DelProductCommand(self.controller))
        self.del_btn.grid(row=20, column=23, columnspan=3, sticky="nsew")

        # Exit protocol override
        self.parent.protocol("WM_DELETE_WINDOW", CloseProductManagementCommand(self.controller))

    def refresh(self):
        self.products_var = self.controller.products
        self.item_list.set_items(self.products_var)
