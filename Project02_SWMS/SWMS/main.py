from tkinter import *
from config import *
from Views.importAllViews import *
from Models.Data.saveData import save_all_data
from Models.Db.fakeDB import load_and_create_users
from Services.tkinterServices import *


def logout(screen):
    screen.destroy()
    main()


def main():
    # load users from file
    status = load_and_create_users()

    if "Fail" in status:
        return
    if status != "Success":
        create_msg("Warning!", status)
    # save to file if new users have been created
    save_all_data()
    # reset the user on startup
    user = "fake"
    # set the user after the login process
    user = log_in()

    if user == "fake":
        return

    # initialize the main screen
    screen = Tk()
    x = (screen.winfo_screenwidth() / 2) - (RES_WIDTH / 2)
    y = (screen.winfo_screenheight() / 2) - (RES_HEIGHT / 2)
    screen.geometry(f"{RES_WIDTH}x{RES_HEIGHT}+{int(x)}+{int(y)}")
    screen.title("Simple Warehouse Management System")

    setup_grid(screen, RES_WIDTH, RES_HEIGHT, 6, 6)

    Label(screen, text=f"Hello {user.user_name}!", font=("Arial", 12), name="user_section").grid(row=0, column=0)
    Button(screen, text="Logout", font=("Arial", 12, "bold"),
           bg="coral", name="logout_btn", command=lambda: logout(screen)).grid(row=0, column=5)

    # render user buttons
    Label(screen, text="Main Operations", font=("Arial", 16, "bold")) \
        .grid(row=1, column=0, columnspan=6, sticky="we")
    Button(screen, width=15, text="Stock", font=("Arial", 12), bg="lightgreen", name="stock_btn",
           command=lambda: stock_window()).grid(row=2, column=1)
    Button(screen, width=15, text="History", font=("Arial", 12), bg="lightgreen", name="history_btn",
           command=lambda: history_window()).grid(row=2,
                                                  column=2)
    Button(screen, width=15, text="Sell", font=("Arial", 12), bg="lightgreen", name="sell_btn",
           command=lambda: sell_window()).grid(row=2, column=3)
    Button(screen, width=15, text="Buy", font=("Arial", 12), bg="lightgreen", name="buy_btn",
           command=lambda: buy_window()).grid(row=2, column=4)

    # render admin buttons
    if user.user_type == "Administrator":
        Label(screen, text="Administrator Options", font=("Arial", 16, "bold")) \
            .grid(row=3, column=0, columnspan=6, sticky="we")
        Button(screen, width=15, text="Users", font=("Arial", 12),
               bg="lightblue", name="users_btn",
               command=lambda: users_window()).grid(row=4, column=1, columnspan=2)
        Button(screen, width=15, text="New Warehouse", font=("Arial", 12),
               bg="lightblue", name="new_whs_btn",
               command=lambda: new_whs_window()).grid(row=4, column=3, columnspan=2)
        Button(screen, width=15, text="New Client", font=("Arial", 12),
               bg="lightblue", name="new_client_btn",
               command=lambda: new_client_window()).grid(row=5, column=1)
        Button(screen, width=15, text="New Supplier", font=("Arial", 12),
               bg="lightblue", name="new_supplier_btn",
               command=lambda: new_supplier_window()).grid(row=5, column=2, columnspan=2)
        Button(screen, width=15, text="New Product", font=("Arial", 12),
               bg="lightblue", name="new_product_btn",
               command=lambda: new_product_window()).grid(row=5, column=4)

    screen.mainloop()
    save_all_data()


main()
