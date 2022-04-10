from tkinter import ttk

from controler.sales_controller import SalesController
from view.base_view import BaseView
from view.commands.transaction_commands.del_invoice_command import DelInvCommand
from view.commands.transaction_commands.generate_invoice_command import GenInvCommand
from view.commands.transaction_commands.preview_invoice_command import PreviewInvCommand
from view.components.item_list import ItemList

from view.commands.transaction_commands.close_transactions_command import CloseTransactionsCommand
from view.components.transactions_item_list import TransactionItemList


class TransactionsView(BaseView):
    def __init__(self, parent, page_name, controller: SalesController, open_views,
                 resolution: tuple = (1280, 728), grid_rows=30, grid_cols=30, icon=None):
        super().__init__(parent, page_name, resolution, grid_rows, grid_cols, icon)
        self.parent = parent
        self.controller = controller
        self.open_views = open_views

        # Transactions ItemList
        self.transactions_var = self.controller.transactions
        self.item_list = TransactionItemList(self.parent, self.transactions_var, 7, 4, colspan=self.cols - 9, rowspan=8)

        # Buttons
        self.create_btn = ttk.Button(self.parent, text="Generate Invoice", command=GenInvCommand(self.controller))
        self.create_btn.grid(row=20, column=6, columnspan=3, sticky="nsew")

        self.edit_btn = ttk.Button(self.parent, text="Preview Invoice", command=PreviewInvCommand(self.controller))
        self.edit_btn.grid(row=20, column=13, columnspan=3, sticky="nsew")

        self.edit_btn = ttk.Button(self.parent, text="Delete Invoice", command=DelInvCommand(self.controller))
        self.edit_btn.grid(row=20, column=20, columnspan=3, sticky="nsew")


        # Exit protocol override
        self.parent.protocol("WM_DELETE_WINDOW", CloseTransactionsCommand(self.controller))

    def refresh(self):
        self.transactions_var = self.controller.transactions
        self.item_list.set_items(self.transactions_var)
