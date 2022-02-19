import tkinter as tk


def create_gui(root):
    header = tk.Label(root, fg="black", justify="center", text="sample header",
                      name="header", font=("Arial", 25, "bold"))
    header.place(rely=0, relx=0, relheight=0.1, relwidth=1)

    home = tk.Label(root, cursor="hand2", justify="center", text="HOME", name="nav_home",
                    relief="raised", borderwidth=5, font=("Arial", 15, "bold"))
    home.place(rely=0.15, relx=0.03, relwidth=0.13, relheight=0.05)

    cost_centre = tk.Label(root, cursor="hand2", justify="center", text="Cost Centre",
                           name="nav_cost_centre", relief="raised", borderwidth=5, font=("Arial", 15, "bold"))
    cost_centre.place(rely=0.25, relx=0.03, relwidth=0.13, relheight=0.05)

    cartridges = tk.Label(root, cursor="hand2", justify="center", text="Cartridges",
                          name="nav_cartridges", relief="raised", borderwidth=5, font=("Arial", 15, "bold"))
    cartridges.place(rely=0.35, relx=0.03, relwidth=0.13, relheight=0.05)

    printers = tk.Label(root, cursor="hand2", justify="center", text="Printers",
                        name="nav_printers", relief="raised", borderwidth=5, font=("Arial", 15, "bold"))
    printers.place(rely=0.45, relx=0.03, relwidth=0.13, relheight=0.05)

    users = tk.Label(root, cursor="hand2", justify="center", text="Users",
                     name="nav_users", relief="raised", borderwidth=5, font=("Arial", 15, "bold"))
    users.place(rely=0.55, relx=0.03, relwidth=0.13, relheight=0.05)

    transactions = tk.Label(root, cursor="hand2", justify="center", text="Transactions",
                            name="nav_transactions", relief="raised", borderwidth=5, font=("Arial", 15, "bold"))
    transactions.place(rely=0.65, relx=0.03, relwidth=0.13, relheight=0.05)

    body = tk.Canvas(root, name="body")
    body.place(rely=0.15, relx=0.2, relwidth=0.8, relheight=0.9)
