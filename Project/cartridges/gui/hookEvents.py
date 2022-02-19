from gui.pages.home import home_btn
from gui.pages.costCentre import nav_cc
from gui.pages.cartridges import nav_crt
from gui.pages.printers import nav_prn
from gui.pages.users import nav_users
from gui.pages.transactions import nav_trans


def hook_events_to_gui(root, tk):
    home = root.nametowidget("nav_home")
    home.bind("<Button-1>", lambda e: home_btn(root, tk))

    cost_centre = root.nametowidget("nav_cost_centre")
    cost_centre.bind("<Button-1>", lambda e: nav_cc(root, tk))

    cartridges = root.nametowidget("nav_cartridges")
    cartridges.bind("<Button-1>", lambda e: nav_crt(root, tk))

    printers = root.nametowidget("nav_printers")
    printers.bind("<Button-1>", lambda e: nav_prn(root, tk))

    users = root.nametowidget("nav_users")
    users.bind("<Button-1>", lambda e: nav_users(root, tk))

    transactions = root.nametowidget("nav_transactions")
    transactions.bind("<Button-1>", lambda e: nav_trans(root, tk))

    home_btn(root, tk)
