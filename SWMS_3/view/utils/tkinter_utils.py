import tkinter as tk


def center_window(root, w=600, h=400):
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))


def setup_grid(root, rows, cols):
    # set rows
    for row in range(rows):
        tk.Grid.rowconfigure(root, row, weight=1)

    # set columns
    for col in range(cols):
        tk.Grid.columnconfigure(root, col, weight=1)


def close_win(root):
    root.destroy()


def close_all(root, systems):
    systems["user_controller"].save()
    systems["warehousing_controller"].save_all()
    systems["sales_controller"].save_all()
    root.destroy()
    exit(0)
