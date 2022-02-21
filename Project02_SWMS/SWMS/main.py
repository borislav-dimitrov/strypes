from tkinter import *
import config as CFG
import Views.importAllViews as Views
import Models.Data.saveData as Save
import Models.Db.fakeDB as DB
import Services.tkinterServices as Tkserv
import Services.dateServices as Dateserv


def logout(screen):
    screen.destroy()
    main()


def main():
    # clear opened windows
    CFG.OPENED = []
    # load users from file
    # Todo - this may be logged in log file
    status = DB.load_and_create_users()
    DB.load_all_entities()

    if "Fail" in status:
        return
    if status != "Success":
        Tkserv.create_msg("Warning!", status)
    # save to file if new users have been created
    Save.save_all_data()
    # reset the user on startup
    user = "fake"
    # set the user after the login process
    user = Views.log_in()

    if user == "fake":
        return

    DB.curr_user = user
    user.user_last_login = Dateserv.get_time_now()
    # initialize the main screen
    screen = Tk()
    x = (screen.winfo_screenwidth() / 2) - (CFG.RES_WIDTH / 2)
    y = (screen.winfo_screenheight() / 2) - (CFG.RES_HEIGHT / 2)
    screen.geometry(f"{CFG.RES_WIDTH}x{CFG.RES_HEIGHT}+{int(x)}+{int(y)}")
    screen.title("Simple Warehouse Management System")

    Tkserv.setup_grid(screen, CFG.RES_WIDTH, CFG.RES_HEIGHT, 6, 6)

    Label(screen, text=f"Hello {user.user_name}!", font=("Arial", 12), name="user_section").grid(row=0, column=0)
    Button(screen, text="Logout", font=("Arial", 12, "bold"),
           bg="coral", name="logout_btn", command=lambda: logout(screen)).grid(row=0, column=5)

    # render user buttons
    Label(screen, text="Main Operations", font=("Arial", 16, "bold")) \
        .grid(row=1, column=0, columnspan=6, sticky="we")
    Button(screen, width=15, text="Stock", font=("Arial", 12), bg="lightgreen", name="stock_btn",
           command=lambda: Views.stock_window()).grid(row=2, column=1)
    Button(screen, width=15, text="History", font=("Arial", 12), bg="lightgreen", name="history_btn",
           command=lambda: Views.history_window()).grid(row=2,
                                                        column=2)
    Button(screen, width=15, text="Sell", font=("Arial", 12), bg="lightgreen", name="sell_btn",
           command=lambda: Views.sell_window()).grid(row=2, column=3)
    Button(screen, width=15, text="Buy", font=("Arial", 12), bg="lightgreen", name="buy_btn",
           command=lambda: Views.buy_window()).grid(row=2, column=4)

    # render admin buttons
    if user.user_type == "Administrator":
        Label(screen, text="Administrator Options", font=("Arial", 16, "bold")) \
            .grid(row=3, column=0, columnspan=6, sticky="we")
        Button(screen, width=15, text="Users", font=("Arial", 12),
               bg="lightblue", name="users_btn",
               command=lambda: Views.users_window(screen)).grid(row=4, column=1, columnspan=2)
        Button(screen, width=15, text="Warehouses", font=("Arial", 12),
               bg="lightblue", name="new_whs_btn",
               command=lambda: Views.new_whs_window()).grid(row=4, column=3, columnspan=2)
        Button(screen, width=15, text="Clients", font=("Arial", 12),
               bg="lightblue", name="new_client_btn",
               command=lambda: Views.new_client_window()).grid(row=5, column=1)
        Button(screen, width=15, text="Suppliers", font=("Arial", 12),
               bg="lightblue", name="new_supplier_btn",
               command=lambda: Views.new_supplier_window(screen)).grid(row=5, column=2, columnspan=2)
        Button(screen, width=15, text="Products", font=("Arial", 12),
               bg="lightblue", name="new_product_btn",
               command=lambda: Views.products_window(screen)).grid(row=5, column=4)

    screen.mainloop()
    Save.save_all_data()


main()
