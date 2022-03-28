import Model.DataBase.my_db as db
import Model.Modules.all_modules as Modules
import Views.all_views as views
import tkinter as tk

# region TODOs
"""
    user:
        asd / "123456Aa!"
        
    Add my firm informaton load/save/reload in counterparties module and include it in db.startup
    modify invoices
        inv number to be int
        when done with invoices hook invoices to transactions
"""


# endregion

def starting_up():
    db.startup()
    login_screen = tk.Tk()
    login = views.MyLogin(login_screen, "Login", "Login", 800, 400, 30, 30)
    login_screen.mainloop()
    print("App is running!\n\n")


def exit_():
    db.on_exit()
    quit()


def logout():
    db.on_exit()
    main()


def main():
    starting_up()
    if not db.curr_user:
        # TODO message
        exit_()

    home_screen = tk.Tk()
    home = views.MyHome(home_screen, "Home", "Simple Warehouse Management System (SWMS)", 1366, 900, 30, 30)
    home_screen.mainloop()

    if home.logging_out:
        # TODO logout
        logout()
    elif home.exiting:
        # TODO log maybe
        exit_()

    print("\n\nApp is closing!")


if __name__ == '__main__':
    main()
