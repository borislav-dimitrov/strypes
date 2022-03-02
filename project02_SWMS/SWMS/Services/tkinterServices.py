from tkinter import *
from tkinter import messagebox
import config as CFG
from Views.onFirstStart import FirstUser
from Services.userServices import encrypt_pwd


def create_custom_msg(m_screen, title, message, w=400, h=150):
    root = Toplevel(m_screen)
    root.title(title)
    x = (root.winfo_screenwidth() / 2) - (w / 2)
    y = (root.winfo_screenheight() / 2) - (h / 2)
    root.geometry(f"{w}x{h}+{int(x)}+{int(y)}")

    msg = Label(root, text=message, font=("Arial", 14, "bold"), wraplength=w)
    if "warning" in title.lower():
        msg.config(fg="red")
    msg.pack(anchor="n", side="top")
    btn = Button(root, text="Ok", font=("Arial", 12, "bold"), width=10,
                 command=lambda: close_window(m_screen, root))
    if "warning" in title.lower():
        btn.config(bg="coral")
    else:
        btn.config(bg="lightblue")
    btn.pack(anchor="s", side="bottom", pady=10)

    root.mainloop()


def create_msg(title, message):
    messagebox.showinfo(title=title, message=message)


def setup_grid(screen, width, height, columns, rows):
    # set rows
    for row in range(rows):
        screen.grid_rowconfigure(row, minsize=height / rows)

    # set columns
    for col in range(columns):
        screen.grid_columnconfigure(col, minsize=width / columns)


def create_drop_down(screen, variable, collection, comm, r, c, rspan=None, cspan=None, stick="", padx=(0, 0),
                     pady=(0, 0), width=-1):
    dropdown = OptionMenu(screen, variable, *collection, command=comm)
    dropdown.config(bg="lightgray")
    if width != -1:
        dropdown.config(width=width)
    dropdown.grid(row=r, column=c, rowspan=rspan, columnspan=cspan, sticky=stick, padx=padx, pady=pady)
    return dropdown


def close_window(main, current):
    # on closing window show the last window
    current.destroy()
    main.deiconify()


def create_preview(screen, data, width=CFG.REG_WIDTH, height=CFG.RES_HEIGHT / 2,
                   rows=30, columns=3, cell_width=0):
    # If cell width is not 0 , the cells will be auto resized by the columns

    parent = Canvas(screen, width=width, height=height)
    parent.grid(row=1, column=0)

    canvas_frame = Frame(parent)
    canvas_frame.grid(row=2, column=0, pady=(5, 0), sticky="nw")
    canvas_frame.grid_rowconfigure(0, weight=1)
    canvas_frame.grid_columnconfigure(0, weight=1)
    canvas_frame.grid_propagate(False)

    canvas = Canvas(canvas_frame)
    canvas.grid(row=0, column=0, sticky="news")

    # Setup scrollbars
    vsb = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky="ns")
    hsb = Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
    hsb.grid(row=1, column=0, sticky="we")
    canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # Fill the info
    info_frame = Frame(canvas)

    # Set up the grid for the auto-sized variant
    if cell_width == 0:
        setup_grid(info_frame, width - 30, height, columns, rows)

    canvas.create_window((0, 0), window=info_frame, anchor="nw")
    for row in range(len(data)):
        for col in range(len(data[0])):
            if row == 0:
                label = Label(info_frame, fg='red',
                              font=('Arial', 12, 'bold'), relief="solid", borderwidth=1)
            else:
                label = Label(info_frame, fg='black',
                              font=('Arial', 12), relief="solid", borderwidth=1)
            if cell_width != 0:
                label.config(width=cell_width, text=data[row][col])
                label.grid(row=row, column=col, sticky="w")
            else:
                label.config(text=data[row][col])
                label.grid(row=row, column=col, sticky="we")

    # Update frame idle tasks to let tkinter calc label sizes
    info_frame.update_idletasks()

    # Resize the canvas
    canvas_frame.config(width=width, height=height)

    # Set the canvas scrolling region
    canvas.config(scrollregion=canvas.bbox("all"))


def create_listbox(parent, name, row, column, data, width=50, height=10, rowspan=1, columnspan=1, sticky="wens",
                   padx=(0, 0), pady=(0, 0)):
    lb_holder = Frame(parent, name=f"{name}_frame")
    lb_holder.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, padx=padx, pady=pady)

    lb_variable = StringVar()
    list_box = Listbox(lb_holder, name=name, listvariable=lb_variable, width=width, height=height)
    list_box.grid(row=0, column=0, sticky="ew")

    if len(data) > 0:
        for item in data:
            list_box.insert(END, item)

    v_scroll = Scrollbar(lb_holder, orient="vertical")
    v_scroll.grid(row=0, column=1, sticky="ns")

    list_box.config(yscrollcommand=v_scroll.set)
    v_scroll.config(command=list_box.yview)

    return list_box, lb_variable
