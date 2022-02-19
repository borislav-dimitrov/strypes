import helpers.tkinterHelpers as tkHelp


def home_btn(root, tk):
    tkHelp.clear_body(root)
    body = root.nametowidget("body")
    # change header
    header = root.nametowidget("header")
    header.config(text="Home Menu")

    # welcome info
    welcome = tk.Label(body, text="Welcome to my home screen =]", font=("Arial", 16, "bold"))
    welcome.grid(row=0, column=0, sticky="we")
