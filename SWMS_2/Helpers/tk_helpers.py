import tkinter as tk


def setup_grid(m_screen, rows, cols, height, width):
    # set rows
    for row in range(rows):
        m_screen.grid_rowconfigure(row, minsize=height / rows)

    # set columns
    for col in range(cols):
        m_screen.grid_columnconfigure(col, minsize=width / cols)


def close_window(main, current):
    # TODO on closing window show the last window
    current.destroy()
    main.deiconify()


def create_custom_msg(m_screen, title, message):
    """
    Create custom message\n
    :param m_screen: the calling tkinter root object (screen)
    :param title: title for the popup message
    :param message: text message to preview
    :return: None
    """
    root = tk.Toplevel(m_screen)
    root.title(title)
    w = 400
    h = 150
    x = (root.winfo_screenwidth() / 2) - (w / 2)
    y = (root.winfo_screenheight() / 2) - (h / 2)
    root.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
    icon = "./Resources/images/popups/i.ico"
    color = "lightblue"
    bg_img = tk.PhotoImage(file="./Resources/images/popups/i_bg.png")

    if "warning" in title.lower():
        color = "coral"
        icon = "./Resources/images/popups/w.ico"
        bg_img = tk.PhotoImage(file="./Resources/images/popups/w_bg.png")

    root.iconbitmap(icon)
    root.resizable(False, False)
    root.attributes('-topmost', True)

    canvas = tk.Canvas(root, width=w, height=h)
    canvas.pack(fill="both")
    canvas.create_image(0, 0, image=bg_img, anchor="nw")
    canvas.create_text(w / 2, 50, text=message, font=("Arial", 14, "bold"), fill="white", width=w - 100)
    btn = tk.Button(canvas, text="Ok", font=("Arial", 12, "bold"), width=10,
                    command=lambda: close_window(m_screen, root), bg=color)
    canvas.create_window(w / 2, h-10, anchor="s", window=btn)

    root.mainloop()
