import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Iterable

import view.utils.tkinter_utils as tkutil

DEFAULT_ENTRY_WIDTH_PX = 250


class ItemForm(tk.Toplevel):
    def __init__(self, parent, item, controller, width=600, height=400, edit=False):
        super().__init__(parent)
        self.parent = parent
        self.item = item
        self.controller = controller
        self.edit = edit

        self.frame = ttk.Frame(self, padding="30 30 30 30")
        self.title("Add Book")
        self.frame.grid(row=0, column=0, sticky="nsew")
        tkutil.center_window(self, width, height)

        self.models = []
        self.types = []
        self.entries = []

        self.columns = tuple(self.item.__dict__.keys())

        for i, col in enumerate(self.columns):
            # add view models
            attr = getattr(self.item, col)
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

            # add labels
            ttk.Label(self.frame, text=col.title(), justify="left").grid(column=0, row=i, sticky="we")

            # add entries
            if col == "password":
                entry = ttk.Entry(self.frame, textvariable=model, show="*")
                if self.edit:
                    plain_pwd = self.controller.service._pwd_mgr.decrypt_pwd(getattr(item, col))
                    print(plain_pwd, 1)
                    entry.delete(0, "end")
                    entry.insert(0, plain_pwd)
            else:
                entry = ttk.Entry(self.frame, textvariable=model)
                # if self.edit:
                #     entry.insert(0, getattr(item, col))
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
        for i, col in enumerate(self.columns):
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

        info = list(info.__dict__.values())
        id_ = info.pop(0)
        if self.edit:
            info.append(id_)
            result = self.controller.update_user(*info)
        else:
            result = self.controller.create_user(*info)

        if isinstance(result, cls):
            self.dismiss()
            if self.edit:
                messagebox.showinfo("Info", f"User {result.name} updated successfully!", parent=self.parent)
            else:
                messagebox.showinfo("Info", f"User {result.name} created successfully!", parent=self.parent)
        else:
            messagebox.showwarning("Warning!", result, parent=self)

    def reset(self):
        for entry in self.entries:
            entry.delete(0, "end")

    def dismiss(self):
        self.grab_release()
        self.destroy()
