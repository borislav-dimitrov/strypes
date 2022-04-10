import tkinter as tk
from tkinter import ttk
import view.utils.tkinter_utils as tkutil
from model.entities.product import Product

from view.base_view import BaseView

from controler.sales_controller import SalesController

# Commands
from view.commands.sales_commands.add_item_to_cart_command import AddItemToCartCommand
from view.commands.sales_commands.clear_cart_command import ClearCartCommand
from view.commands.sales_commands.close_sales_command import CloseSalesCommand
from view.commands.sales_commands.rem_item_from_cart_command import RemItemFromCartCommand
from view.commands.sales_commands.sell_command import SellCommand
from view.commands.warehouse_commands.generate_wh_treeview_command import GenWhProductsTreeViewCommand
from view.components.trade_item_list import TradeItemList


class SalesView(BaseView):
    def __init__(self, parent, page_name, sales_controller: SalesController, open_views,
                 resolution: tuple = (1280, 728), grid_rows=30, grid_cols=30, icon=None):
        super().__init__(parent, page_name, resolution, grid_rows, grid_cols, icon)
        self.parent = parent
        self.controller = sales_controller
        self.open_views = open_views

        # Warehouses List
        self.wh_lbl = ttk.Label(self.parent, text="Chose Warehouse", anchor="center", font=self.text_bold)
        self.wh_lbl.grid(row=8, column=5, columnspan=3, sticky="we")

        self.warehouses_list = ["None", *self.controller.warehouses_for_dropdown()]
        self.warehouses_var = tk.StringVar()
        self.warehouses_var.set(self.warehouses_list[0])
        self.warehouses_dropdown = tk.OptionMenu(self.parent, self.warehouses_var, *self.warehouses_list,
                                                 command=GenWhProductsTreeViewCommand(self.controller, self))
        self.warehouses_dropdown.grid(row=9, column=5, columnspan=3, sticky="we")

        # Sellable Products Treeview
        self.treeview_var = self.controller.find_all_products_in_warehouse(None)
        self.treeview = TradeItemList(self.parent, self.treeview_var, 10, 5, colspan=10)

        # Add to cart
        self.amount_lbl = ttk.Label(self.parent, text="Amount", font=self.text_bold)
        self.amount_lbl.grid(row=8, column=10, sticky="we")

        self.amount_entry = ttk.Entry(self.parent, width=10)
        self.amount_entry.grid(row=9, column=10, columnspan=2, sticky="w")

        self.add_btn = ttk.Button(self.parent, text="Add >>", command=AddItemToCartCommand(self.controller))
        self.add_btn.grid(row=9, column=11, sticky="e")

        # Rem from cart btn
        self.rem_btn = ttk.Button(self.parent, text="<< Remove", command=RemItemFromCartCommand(self.controller))
        self.rem_btn.grid(row=9, column=16, sticky="w")

        # Clients List
        self.cli_lbl = ttk.Label(self.parent, text="Chose Client", anchor="center", font=self.text_bold)
        self.cli_lbl.grid(row=8, column=21, columnspan=3, sticky="we")

        self.clients_list = self.controller.gen_clients_for_treeview()
        self.clients_var = tk.StringVar()
        self.clients_var.set(self.clients_list[0])
        self.clients_dropdown = tk.OptionMenu(self.parent, self.clients_var, *self.clients_list)
        self.clients_dropdown.grid(row=9, column=21, columnspan=3, sticky="we")

        # Shopping Cart
        self.shopping_cart_var = []
        self.shopping_cart = TradeItemList(self.parent, self.shopping_cart_var, 10, 16, colspan=10)

        # Total Price Label
        self.total_price_var = tk.StringVar()
        self.total_price_var.set("Total Price: 0.0 BGN")
        self.total_lbl = ttk.Label(self.parent, textvariable=self.total_price_var, font=self.text_bold)
        self.total_lbl.grid(row=15, column=5, rowspan=2, columnspan=3, sticky="nsew")

        # Sell Button
        self.sell_btn = ttk.Button(self.parent, text="Sell", command=SellCommand(self.controller))
        self.sell_btn.grid(row=15, column=16, rowspan=2, sticky="nsew")

        # Clear Cart Button
        self.clear_btn = ttk.Button(self.parent, text="Clear", command=ClearCartCommand(self.controller))
        self.clear_btn.grid(row=15, column=22, rowspan=2, sticky="nsew")

        # Exit protocol override
        self.parent.protocol("WM_DELETE_WINDOW", CloseSalesCommand(self.controller))

    def refresh(self):
        GenWhProductsTreeViewCommand(self.controller, self)
        self.treeview.set_items(self.treeview_var)

        self.shopping_cart.set_items(self.shopping_cart_var)
