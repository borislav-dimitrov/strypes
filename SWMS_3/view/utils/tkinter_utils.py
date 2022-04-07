import tkinter as tk


def clear_widgets(root, exceptions: list[tk.Widget]):
    for widget in root.grid_slaves():
        if widget not in exceptions:
            widget.destroy()


def center_window(root, w=600, h=400):
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))


def setup_grid(parent, rows, cols):
    # set rows
    for row in range(rows):
        tk.Grid.rowconfigure(parent, row, weight=1)

    # set columns
    for col in range(cols):
        tk.Grid.columnconfigure(parent, col, weight=1)


def close_all_(root, systems):
    systems["user_controller"].save()
    systems["warehousing_controller"].save_all()
    systems["sales_controller"].save_all()
    root.destroy()
    exit(0)
