import config as CFG
import Services.tkinterServices as TkServ
from tkinter import *
from Controls.salesControls import add_item_to_cart, rem_item_from_cart, clear_cart, sell, on_client_change
from Services.productServices import get_all_sellable_products
import Models.Db.fakeDB as DB


def sell_window(m_screen):
    # Check if another suppliers window is opened
    if "sell" in CFG.OPENED:
        TkServ.create_custom_msg(m_screen, "Warning!", "Sales page is already opened!")
        return

    # Add the window to the opened ones
    if "sell" not in CFG.OPENED:
        CFG.OPENED.append("sell")

    screen = Toplevel(m_screen)
    x = (screen.winfo_screenwidth() / 2) - (CFG.RES_WIDTH / 2)
    y = (screen.winfo_screenheight() / 2) - (CFG.RES_HEIGHT / 2)
    screen.geometry(f"{CFG.RES_WIDTH}x{CFG.RES_HEIGHT}+{int(x)}+{int(y)}")
    screen.title("Sales")
    TkServ.setup_grid(screen, CFG.RES_WIDTH, CFG.RES_HEIGHT, 4, 30)

    # Set header
    Label(screen, name="header_lbl", text="Sales", font=("Ariel", 15, "bold")) \
        .grid(row=0, column=2, columnspan=5, sticky="w")

    # Create Lables
    Label(screen, text="TOTAL PRICE:", font=("Ariel", 13, "bold")) \
        .grid(row=22, column=3, sticky="s", padx=10)
    Label(screen, name="total_price", text="0.0", font=("Ariel", 13, "bold")) \
        .grid(row=23, column=3, sticky="we", padx=10)
    Label(screen, name="sellable_products", text="Sellable Products", font=("Ariel", 12, "bold")) \
        .grid(row=9, column=0, sticky="we")
    Label(screen, name="clients", text="Clients", font=("Ariel", 12, "bold")) \
        .grid(row=9, column=3, sticky="we")
    # Create listbox with all the products that can be added to the cart
    sellable_lb, sellable_items = TkServ.create_listbox(screen, "sellable_lb", row=10, column=0,
                                                        width=25, height=25,
                                                        rowspan=14, columnspan=1,
                                                        data=get_all_sellable_products(DB.products),
                                                        padx=(0, 25), sticky="e")

    # Create listbox with clients
    drop_down_variable = StringVar(screen)
    drop_down_variable.set("None")
    drop_down_options = []
    for client in DB.clients:
        drop_down_options.append(f"{client.client_id} | {client.client_name}")
    sel_client = TkServ.create_drop_down(screen, drop_down_variable, drop_down_options,
                                         lambda a: on_client_change(), 10, 3, stick="we")
    # Figure out a way to name sel_client

    # Create transaction cart
    cart_lb, cart_items = TkServ.create_listbox(screen, "cart_lb", row=10, column=1, width=80, height=25,
                                                rowspan=14, columnspan=2, data=[])

    # Create buttons to manage the cart
    Button(screen, text="Add =>", name="add_to_cart_btn", font=("Arial", 12),
           bg="lightgreen",
           command=lambda: add_item_to_cart(screen, cart_lb, sellable_lb, cart_items)) \
        .grid(row=9, column=1, sticky="w")
    Button(screen, text="<= Remove", name="rem_item_from_cart_btn", font=("Arial", 12),
           bg="coral",
           command=lambda: rem_item_from_cart(screen, cart_lb, sellable_lb, cart_items)) \
        .grid(row=9, column=2, sticky="e", padx=(0, 35))
    Button(screen, text="Clear", width=25, name="clear_cart_btn", font=("Arial", 12, "bold"),
           bg="red", fg="white",
           command=lambda: clear_cart(screen, cart_lb, cart_items)) \
        .grid(row=24, column=1, columnspan=2, sticky="we", padx=(0, 35))
    Button(screen, text="Sell", width=25, name="sell_cart_btn", font=("Arial", 12),
           bg="green",
           command=lambda: sell(screen, cart_lb, cart_items, sellable_items)) \
        .grid(row=24, column=3, sticky="we", padx=10)

    screen.protocol("WM_DELETE_WINDOW", lambda: TkServ.close_and_rem_win_from_opened(screen, "sell"))
    screen.mainloop()
