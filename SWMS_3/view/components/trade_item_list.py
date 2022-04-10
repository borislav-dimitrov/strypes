import tkinter as tk
from tkinter import ttk

from model.entities.product import Product
from model.entities.warehouse import Warehouse

DEFAULT_COLUMN_WIDTH_PX = 140


class TradeItemList:
    def __init__(self, parent, items, row, col, rowspan=None, colspan=None, sticky="nsew", purchase=False):
        super().__init__()
        self.parent = parent
        self.items = items
        self.item_pos_ids = None
        self.purchase = purchase

        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky=sticky)

        if items:
            columns = [key for key in self.items[0].__dict__.keys()]
            columns.remove("assigned_wh")
            if self.purchase:
                columns.remove("quantity")

        else:
            columns = ["id", "name", "type", "buy_price", "sell_price", "quantity"]

        self.tree = ttk.Treeview(self.frame, columns=columns, selectmode='extended', show='headings')

        for column in columns:
            self.tree.heading(column, text=column.title())
            if column == "id":
                self.tree.column(column, width=30)
            elif column == "name":
                self.tree.column(column, width=100)
            elif column == "type":
                self.tree.column(column, width=100)
            elif column == "buy_price":
                self.tree.column(column, width=90)
            elif column == "sell_price":
                self.tree.column(column, width=90)
            elif column == "quantity":
                self.tree.column(column, width=80)
            else:
                self.tree.column(column, width=DEFAULT_COLUMN_WIDTH_PX)

        self.tree.grid(row=0, column=0, sticky="nsew")

        # add vertical scrollbar
        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="nws", padx=0)
        self.tree.configure(yscroll=vsb.set)

        # resize the parent window to show treeview widget
        # self.tree.update_idletasks()
        # self.frame.rowconfigure(0, weight=1, minsize=self.tree.winfo_height())
        # self.frame.columnconfigure(0, weight=1, minsize=self.tree.winfo_width())

        # set items
        if self.items:
            self.set_items(self.items)

    def set_items(self, items):
        def set_item(item):
            values = list(val for val in item.__dict__.values())
            for i, val in enumerate(values):
                if isinstance(val, (list, tuple)):
                    values[i] = ', '.join(val)
                elif isinstance(val, Warehouse):
                    pass
            return self.tree.insert('', tk.END, values=tuple(values))

        if self.item_pos_ids is not None:
            self.tree.delete(*self.item_pos_ids)
        self.items = items
        self.item_pos_ids = list(map(set_item, self.items))
        self.parent.update_idletasks()
        if self.items:
            self.tree.see(self.item_pos_ids[-1])

    def get_selected_items(self):
        items = []
        for sel_item in self.tree.selection():
            items.append(self.tree.item(sel_item, 'values'))
        return items
