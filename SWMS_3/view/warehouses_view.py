import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import view.utils.tkinter_utils as tkutil
from controler.warehousing_controller import WarehousingController
from view.base_view import BaseView
from view.components.item_list import ItemList

# Commands
from view.commands.warehouse_commands.close_warehouses_command import CloseWarehousesCommand
from view.commands.product_commands.move_product_command import MoveProductCommand
from view.commands.warehouse_commands.generate_wh_treeview_command import GenWhProductsTreeViewCommand


class WarehousesView(BaseView):
    def __init__(self, parent, page_name, controller: WarehousingController, open_views,
                 resolution: tuple = (1280, 728), grid_rows=30, grid_cols=30, icon=None):
        super().__init__(parent, page_name, resolution, grid_rows, grid_cols, icon)
        self.parent = parent
        self.controller = controller
        self.open_views = open_views

        # Warehouses List
        self.warehouses_list = ["None", *self.controller.warehouses_for_dropdown]
        self.warehouses_var = tk.StringVar()
        self.warehouses_var.set(self.warehouses_list[0])
        self.warehouses_dropdown = tk.OptionMenu(self.parent, self.warehouses_var, *self.warehouses_list,
                                                 command=GenWhProductsTreeViewCommand(self.controller, self))
        self.warehouses_dropdown.grid(row=5, column=self.cols // 2 - 3, columnspan=5, sticky="we")

        # ItemList
        self.treeview_var = self.controller.module.find_all_products_in_warehouse(None)
        self.treeview = ItemList(self.parent, self.treeview_var, 7, 2, colspan=self.cols - 5)

        # Move Button
        self.move_btn = ttk.Button(self.parent, text="Move Product", command=MoveProductCommand(self.controller))
        self.move_btn.grid(row=15, column=self.cols // 2 - 3, columnspan=5, sticky="we")

        # Exit protocol override
        self.parent.protocol("WM_DELETE_WINDOW", CloseWarehousesCommand(self.controller))

    def refresh(self):
        GenWhProductsTreeViewCommand(self.controller, self)
        self.treeview.set_items(self.treeview_var)
