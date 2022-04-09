import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Iterable

import view.utils.tkinter_utils as tkutil
from model.entities.counterparty import Counterparty
from model.entities.product import Product
from model.entities.user import User
from model.entities.warehouse import Warehouse

DEFAULT_ENTRY_WIDTH_PX = 250


class ItemForm(tk.Toplevel):
    def __init__(self, parent, item, controller, title="", width=600, height=400, edit=False):
        super().__init__(parent)
        self.parent = parent
        self.item = item
        self.controller = controller
        self.edit = edit

        self.frame = ttk.Frame(self, padding="30 30 30 30")
        self.title(title)
        self.frame.grid(row=0, column=0, sticky="nsew")
        tkutil.center_window(self, width, height)

        self.models = []
        self.types = []
        self.entries = []

        self.columns = tuple(self.item.__dict__.keys())

        for i, col in enumerate(self.columns):
            if isinstance(self.item, Warehouse) and col == "products":  # Don't include products field for warehouses
                continue
            else:
                # Add view models
                attr = getattr(self.item, col)
                if self.edit and isinstance(self.item, Product) and col == "assigned_wh" and attr is not None:
                    # Product assigned warehouse case when editing
                    model = tk.StringVar()
                    model.set(attr.name)
                    self.types.append("str")
                    self.models.append(model)
                elif isinstance(item, Counterparty) and item.type == "Supplier" and col == "description":
                    # Counterparty {Supplier} description case
                    if len(attr) > 0:
                        if len(attr) == 4:
                            value = ", ".join([i if isinstance(i, str) else str(i) for i in attr])
                        else:
                            value = []
                            for product in attr:
                                new_product = ", ".join([i if isinstance(i, str) else str(i) for i in product])
                                value.append(new_product)
                            value = " | ".join(value)
                        self.types.append("str")
                        model = tk.StringVar()
                        model.set(value)
                        self.models.append(model)
                else:
                    if isinstance(attr, int):
                        self.types.append("int")
                    elif isinstance(attr, float):
                        self.types.append("float")
                    elif isinstance(attr, (tuple, list)):
                        self.types.append("list")
                    else:
                        self.types.append("str")
                    model = tk.StringVar()
                    model.set(attr)
                    self.models.append(model)

                # Add labels
                ttk.Label(self.frame, text=col.title(), justify="left").grid(column=0, row=i, sticky="we")

                # Add entries
                if col == "password":
                    entry = ttk.Entry(self.frame, textvariable=model, show="*")
                    if self.edit:
                        plain_pwd = self.controller.module._pwd_mgr.decrypt_pwd(getattr(item, col))
                        entry.delete(0, "end")
                        entry.insert(0, plain_pwd)
                else:
                    entry = ttk.Entry(self.frame, textvariable=model)

                entry.grid(column=1, row=i, sticky="we")

                if col == 'id':
                    entry.configure(state="disabled")
                self.entries.append(entry)

        # make form resizable
        rows, cols = self.frame.grid_size()
        for row in range(rows):
            self.frame.rowconfigure(row, weight=1)
        self.frame.columnconfigure(0, weight=1, minsize=DEFAULT_ENTRY_WIDTH_PX)
        self.frame.columnconfigure(1, weight=1, minsize=DEFAULT_ENTRY_WIDTH_PX)

        # add buttons
        buttons_frame = ttk.Frame(self.frame, padding="20 10 20 10")
        buttons_frame.grid(column=0, row=len(self.columns), columnspan=2, sticky="nsew")

        self.add_button = ttk.Button(buttons_frame, text="Submit", padding=10, command=self.submit)
        self.add_button.grid(column=1, row=0, sticky="ne", padx=40, pady=20)

        self.add_button = ttk.Button(buttons_frame, text="Reset", padding=10, command=self.reset)
        self.add_button.grid(column=2, row=0, sticky="ne", padx=40, pady=20)

        rows, cols = buttons_frame.grid_size()
        for col in range(cols):
            buttons_frame.columnconfigure(col, minsize=100, pad=30)

        # modal - capture visibility
        self.protocol("WM_DELETE_WINDOW", self.dismiss)
        self.transient(self.parent)
        self.wait_visibility()
        self.grab_set()
        self.wait_window()

    def submit(self):
        cls = type(self.item)
        info = list(self.item.__dict__.values())
        id_ = info.pop(0)
        info = cls(*info)
        i = 0
        for col in self.columns:
            if isinstance(self.item, Warehouse) and col == "products":  # Skip warehouse products
                continue
            else:
                self.models[i].set(self.entries[i].get())
                str_val = self.models[i].get()
                if self.types[i] == "int":
                    value = int(str_val)
                elif self.types[i] == "float":
                    value = float(str_val)
                elif self.types[i] == "str":
                    value = str_val
                elif self.types[i] == "list":
                    value = [s.strip() for s in str_val.split(',')]
                setattr(info, col, value)
            i += 1

        info = list(info.__dict__.values())
        id_ = info.pop(0)
        if self.edit:
            info.append(id_)
            result = self.call_controller_update(info)
        else:
            result = self.call_controller_create(info)

        if isinstance(result, cls):
            self.dismiss()

    def reset(self):
        for entry in self.entries:
            entry.delete(0, "end")

    def dismiss(self):
        self.grab_release()
        self.destroy()

    def call_controller_create(self, attributes):
        if isinstance(self.item, User):
            result = self.controller.create_user(*attributes)
        elif isinstance(self.item, Warehouse):
            result = self.controller.create_warehouse(*attributes)
        elif isinstance(self.item, Product):
            result = self.controller.create_product(*attributes)
        elif isinstance(self.item, Counterparty):
            result = self.controller.create_counterparty(*attributes)
        return result

    def call_controller_update(self, attributes):
        if isinstance(self.item, User):
            result = self.controller.update_user(*attributes)
        elif isinstance(self.item, Warehouse):
            result = self.controller.update_warehouse(*attributes)
        elif isinstance(self.item, Product):
            result = self.controller.update_product(*attributes)
        elif isinstance(self.item, Counterparty):
            result = self.controller.update_counterparty(*attributes)
        return result
