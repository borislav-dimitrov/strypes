import tkinter as tk
from config import *


def clear_body(root):
    body = root.nametowidget("body")
    for e in body.grid_slaves():
        e.destroy()


def create_preview(body, data, w=PREV_WIDTH, h=PREV_HEIGHT):
    parent = tk.Canvas(body, width=100, height=500)
    parent.grid(row=1, column=0)

    canvas_frame = tk.Frame(parent)
    canvas_frame.grid(row=2, column=0, pady=(5, 0), sticky="nw")
    canvas_frame.grid_rowconfigure(0, weight=1)
    canvas_frame.grid_columnconfigure(0, weight=1)
    canvas_frame.grid_propagate(False)

    canvas = tk.Canvas(canvas_frame)
    canvas.grid(row=0, column=0, sticky="news")

    # Setup scrollbars
    vsb = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky="ns")
    hsb = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
    hsb.grid(row=1, column=0, sticky="we")
    canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # Fill the info
    info_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=info_frame, anchor="nw")
    for row in range(len(data)):
        for col in range(len(data[0])):
            if row == 0:
                label = tk.Label(info_frame, width=15, fg='blue', bg="lightgray",
                                 font=('Arial', 15), relief="raised", borderwidth=3, anchor="w")
            else:
                label = tk.Label(info_frame, width=15, fg='black',
                                 font=('Arial', 15), relief="raised", borderwidth=3, anchor="w")
            label.config(text=data[row][col])
            label.grid(row=row, column=col)

    # Update frame idle tasks to let tkinter calc label sizes
    info_frame.update_idletasks()

    # Resize the canvas
    canvas_frame.config(width=w, height=h)

    # Set the canvas scrolling region
    canvas.config(scrollregion=canvas.bbox("all"))

