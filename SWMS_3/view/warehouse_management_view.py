import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import view.utils.tkinter_utils as tkutil
from controler.warehousing_controller import WarehousingController
from model.entities.user import User
from model.entities.warehouse import Warehouse
from view.base_view import BaseView
from view.components.item_list import ItemList


class WarehouseManagementView(BaseView):
    def __init__(self, parent, page_name, controller: WarehousingController, resolution: tuple = (1280, 728),
                 grid_rows=30,
                 grid_cols=30, icon=None):
        super().__init__(parent, page_name, resolution, grid_rows, grid_cols, icon)
        self.parent = parent
        self.controller = controller

        # Set controller view
        self.controller.view = self

        # Create GUI

        # Users ItemList
        self.warehouses_var = self.controller.warehouses
        self.item_list = ItemList(self.parent, self.warehouses_var, 7, 2, colspan=self.cols - 5)

        # Create Button
        self.create_btn = ttk.Button(self.parent, text="Create Warehouse",
                                     command=lambda: self.controller.show_add_warehouse())
        self.create_btn.grid(row=20, column=5, columnspan=3, sticky="nsew")

        # Update Button
        self.edit_btn = ttk.Button(self.parent, text="Update Warehouse", command=lambda: self.show_edit_warehouse())
        self.edit_btn.grid(row=20, column=14, columnspan=3, sticky="nsew")

        # Delete Button
        self.del_btn = ttk.Button(self.parent, text="Delete Warehouse", command=lambda: self.del_warehouse())
        self.del_btn.grid(row=20, column=23, columnspan=3, sticky="nsew")

        # Exit protocol override
        self.parent.protocol("WM_DELETE_WINDOW", lambda: self.default_exit())

    def refresh(self):
        self.warehouses_var = self.controller.warehouses
        self.item_list.set_items(self.warehouses_var)

    def show_edit_warehouse(self):
        selected = self.item_list.get_selected_items()
        if len(selected) < 1:
            messagebox.showwarning("Warning!", "Please make a selection first!", parent=self.parent)
        else:
            self.controller.show_edit_warehouse(selected)

    def del_warehouse(self):
        selected = self.item_list.get_selected_items()
        if len(selected) < 1:
            messagebox.showwarning("Warning!", "Please make a selection first!", parent=self.parent)
        else:
            result = self.controller.del_warehouse(selected)
            if isinstance(result, Warehouse):
                messagebox.showinfo("Info!", f"Warehouse {result.name} successfully deleted!", parent=self.parent)
            else:
                messagebox.showwarning("Warning", result, parent=self.parent)
