from tkinter import ttk

from view.base_view import BaseView
from view.components.item_list import ItemList

# Commands
from view.commands.counterparty_commands.close_counterparty_mgmt_command import CloseCounterpartyMgmtCommand
from view.commands.counterparty_commands.del_counterparty_command import DelCounterpartyCommand
from view.commands.counterparty_commands.show_create_counterparty_command import ShowCreateCounterpartyCommand
from view.commands.counterparty_commands.show_update_counterparty_command import ShowUpdateCounterpartyCommand


class CounterpartyManagementView(BaseView):
    def __init__(self, parent, page_name, controller, open_views, resolution: tuple = (1280, 728),
                 grid_rows=30, grid_cols=30, icon=None):
        super().__init__(parent, page_name, resolution, grid_rows, grid_cols, icon)
        self.parent = parent
        self.controller = controller
        self.open_views = open_views

        # Counterparties dropdown
        self.counterparties_var = self.controller.counterparties
        self.item_list = ItemList(self.parent, self.counterparties_var, 7, 2, colspan=self.cols - 5)

        # Create Button
        self.create_btn = ttk.Button(self.parent, text="Create Counterparty",
                                     command=ShowCreateCounterpartyCommand(self.controller))
        self.create_btn.grid(row=20, column=5, columnspan=3, sticky="nsew")

        # Update Button
        self.edit_btn = ttk.Button(self.parent, text="Update Counterparty",
                                   command=ShowUpdateCounterpartyCommand(self.controller))
        self.edit_btn.grid(row=20, column=14, columnspan=3, sticky="nsew")

        # Delete Button
        self.del_btn = ttk.Button(self.parent, text="Delete Counterparty",
                                  command=DelCounterpartyCommand(self.controller))
        self.del_btn.grid(row=20, column=23, columnspan=3, sticky="nsew")

        # Exit protocol override
        self.parent.protocol("WM_DELETE_WINDOW", CloseCounterpartyMgmtCommand(self.controller))

    def refresh(self):
        self.counterparties_var = self.controller.counterparties
        self.item_list.set_items(self.counterparties_var)
