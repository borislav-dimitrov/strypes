import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import view.utils.tkinter_utils as tkutil
from controler.warehousing_controller import WarehousingController
from model.entities.user import User
from model.entities.warehouse import Warehouse
from view.base_view import BaseView
from view.commands.warehouse_commands.close_warehouse_management import CloseWarehouseMgmtCommand
from view.commands.warehouse_commands.del_warehouse_command import DelWhCommand
from view.commands.warehouse_commands.show_create_warehouse_command import ShowCreateWhCommand
from view.commands.warehouse_commands.show_edit_warehouse_command import ShowEditWhCommand
from view.components.item_list import ItemList


class WarehouseManagementView(BaseView):
    def __init__(self, parent, page_name, controller: WarehousingController, open_views,
                 resolution: tuple = (1280, 728), grid_rows=30, grid_cols=30, icon=None):
        super().__init__(parent, page_name, resolution, grid_rows, grid_cols, icon)
        self.parent = parent
        self.controller = controller
        self.open_views = open_views

        # Users ItemList
        self.warehouses_var = self.controller.warehouses
        self.item_list = ItemList(self.parent, self.warehouses_var, 7, 2, colspan=self.cols - 5)

        # Create Button
        self.create_btn = ttk.Button(self.parent, text="Create Warehouse", command=ShowCreateWhCommand(self.controller))
        self.create_btn.grid(row=20, column=5, columnspan=3, sticky="nsew")

        # Update Button
        self.edit_btn = ttk.Button(self.parent, text="Update Warehouse", command=ShowEditWhCommand(self.controller))
        self.edit_btn.grid(row=20, column=14, columnspan=3, sticky="nsew")

        # Delete Button
        self.del_btn = ttk.Button(self.parent, text="Delete Warehouse", command=DelWhCommand(self.controller))
        self.del_btn.grid(row=20, column=23, columnspan=3, sticky="nsew")

        # Exit protocol override
        self.parent.protocol("WM_DELETE_WINDOW", CloseWarehouseMgmtCommand(self.controller))

    def refresh(self):
        self.warehouses_var = self.controller.warehouses
        self.item_list.set_items(self.warehouses_var)

