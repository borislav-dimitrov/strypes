import helpers.tkinterHelpers as tkHelp


def nav_trans(root, tk):
    tkHelp.clear_body(root)
    body = root.nametowidget("body")
    # change header
    header = root.nametowidget("header")
    header.config(text="Transactions Menu")
    print("transactions")
