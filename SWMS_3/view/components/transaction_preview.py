import tkinter as tk
from tkinter import ttk

import view.utils.tkinter_utils as tkutil
from model.entities.counterparty import Counterparty
from model.entities.invoices import Invoice
from model.entities.transaction import Transaction

DEFAULT_ENTRY_WIDTH_PX = 250


class TransactionPreview(tk.Toplevel):
    def __init__(self, parent, item: Transaction, controller, title="Transaction Preview", width=600, height=300):
        super().__init__(parent)
        self.parent = parent
        self.item = item
        self.controller = controller

        self.frame = ttk.Frame(self, padding="30 30 30 30")
        self.title(title)
        self.frame.grid(row=0, column=0, sticky="nsew")
        tkutil.center_window(self, width, height)

        fields = self.item.__dict__.keys()

        row = 0
        for field in fields:
            # Create key label
            ttk.Label(self.frame, text=field + ":").grid(row=row, column=2, sticky="we")

            # Create data label
            if isinstance(getattr(self.item, field), Counterparty):
                cpty = getattr(self.item, field)
                ttk.Label(self.frame, text=f"{cpty.id}, {cpty.name}, {cpty.payment_nr}").grid(row=row, column=6, sticky="we", padx=75)
                row += 1
            elif field == "assets":
                assets = getattr(self.item, field)
                for asset in assets:
                    ttk.Label(self.frame, text=", ".join((str(i) for i in asset.__dict__.values()))).grid(row=row, column=6, sticky="we", padx=75)
                    row += 1
            elif field == "invoice":
                inv = getattr(self.item, field)
                if inv is None:
                    ttk.Label(self.frame, text="None").grid(row=row, column=6, sticky="we", padx=75)
                    row += 1
                elif isinstance(inv, Invoice):
                    ttk.Label(self.frame, text=f"{inv.id}, {inv.number}, {inv.status}").grid(row=row, column=6, sticky="we", padx=75)
                    row += 1
            else:
                ttk.Label(self.frame, text=getattr(self.item, field)).grid(row=row, column=6, sticky="we", padx=75)
                row += 1

        # modal - capture visibility
        self.protocol("WM_DELETE_WINDOW", self.dismiss)
        self.transient(self.parent)
        self.wait_visibility()
        self.grab_set()
        self.wait_window()

    def dismiss(self):
        self.grab_release()
        self.destroy()
