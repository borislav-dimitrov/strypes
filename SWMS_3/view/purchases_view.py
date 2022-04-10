import tkinter as tk
from tkinter import ttk

from view.base_view import BaseView

from controler.sales_controller import SalesController

# Commands
from view.commands.purchase_commands.buy_command import BuyCommand
from view.commands.purchase_commands.clear_cart_command import ClearCartCommand
from view.commands.purchase_commands.add_to_cart_command import AddToCartCommand
from view.commands.purchase_commands.close_pur_command import ClosePurCommand
from view.commands.purchase_commands.on_supplier_change_command import OnSupplierChange
from view.commands.purchase_commands.rem_from_cart_command import RemFromCartCommand
from view.components.transactions_item_list import TransactionItemList


class PurchasesView(BaseView):
    def __init__(self, parent, page_name, sales_controller: SalesController, open_views,
                 resolution: tuple = (1280, 728), grid_rows=30, grid_cols=30, icon=None):
        super().__init__(parent, page_name, resolution, grid_rows, grid_cols, icon)
        self.parent = parent
        self.controller = sales_controller
        self.open_views = open_views

        # Suppliers List
        self.wh_lbl = ttk.Label(self.parent, text="Chose Supplier", anchor="center", font=self.text_bold)
        self.wh_lbl.grid(row=8, column=5, columnspan=3, sticky="we")

        self.suppliers_list = [*self.controller.suppliers_for_dropdown()]
        self.suppliers_var = tk.StringVar()
        self.suppliers_var.set(self.suppliers_list[0])
        self.warehouses_dropdown = tk.OptionMenu(self.parent, self.suppliers_var, *self.suppliers_list,
                                                 command=OnSupplierChange(self.controller))
        self.warehouses_dropdown.grid(row=9, column=5, columnspan=3, sticky="we")

        # Available Products Treeview
        self.treeview_var = self.controller.get_supplier_products()
        self.treeview = TransactionItemList(self.parent, self.treeview_var, 10, 5, colspan=10, purchase=True)

        # Add to cart
        self.amount_lbl = ttk.Label(self.parent, text="Amount", font=self.text_bold)
        self.amount_lbl.grid(row=8, column=10, sticky="we")

        self.amount_entry = ttk.Entry(self.parent, width=10)
        self.amount_entry.grid(row=9, column=10, columnspan=2, sticky="w")

        self.add_btn = ttk.Button(self.parent, text="Add >>", command=AddToCartCommand(self.controller))
        self.add_btn.grid(row=9, column=11, sticky="e")

        # Rem from cart btn
        self.rem_btn = ttk.Button(self.parent, text="<< Remove", command=RemFromCartCommand(self.controller))
        self.rem_btn.grid(row=9, column=16, sticky="w")

        # Shopping Cart
        self.shopping_cart_var = []
        self.shopping_cart = TransactionItemList(self.parent, self.shopping_cart_var, 10, 16, colspan=10)

        # Total Price Label
        self.total_price_var = tk.StringVar()
        self.total_price_var.set("Total Price: 0.0 BGN")
        self.total_lbl = ttk.Label(self.parent, textvariable=self.total_price_var, font=self.text_bold)
        self.total_lbl.grid(row=15, column=5, rowspan=2, columnspan=3, sticky="nsew")

        # Sell Button
        self.sell_btn = ttk.Button(self.parent, text="Buy", command=BuyCommand(self.controller))
        self.sell_btn.grid(row=15, column=16, rowspan=2, sticky="nsew")

        # Clear Cart Button
        self.clear_btn = ttk.Button(self.parent, text="Clear", command=ClearCartCommand(self.controller))
        self.clear_btn.grid(row=15, column=22, rowspan=2, sticky="nsew")

        # Exit protocol override
        self.parent.protocol("WM_DELETE_WINDOW", ClosePurCommand(self.controller))

    def refresh(self):
        OnSupplierChange(self.controller)
        self.treeview.set_items(self.treeview_var)

        self.shopping_cart.set_items(self.shopping_cart_var)
