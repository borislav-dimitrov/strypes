from tkinter import *
import config as CFG
import Services.tkinterServices as TkServ
from Controls.stockControls import stock_by_wh, stock_by_product


def stock_window(m_screen):
    # Check if another suppliers window is opened
    if "stock" in CFG.OPENED:
        TkServ.create_custom_msg(m_screen, "Warning!", "View Stock page is already opened!")
        return

    # Add the window to the opened ones
    if "stock" not in CFG.OPENED:
        CFG.OPENED.append("stock")

    screen = Toplevel(m_screen)
    x = (screen.winfo_screenwidth() / 2) - (CFG.RES_WIDTH / 2)
    y = (screen.winfo_screenheight() / 2) - (CFG.RES_HEIGHT / 2)
    screen.geometry(f"{CFG.RES_WIDTH}x{CFG.RES_HEIGHT}+{int(x)}+{int(y)}")
    screen.title("Clients")
    TkServ.setup_grid(screen, CFG.RES_WIDTH, CFG.RES_HEIGHT, 5, 30)

    # Set header
    Label(screen, name="header_lbl", text="View Stock", font=("Ariel", 15, "bold")) \
        .grid(row=0, column=2, columnspan=5, sticky="w")

    # Create Buttons
    Button(screen, name="stock_by_wh_btn", text="By Warehouses", font=("Ariel", 12),
           width=25, bg="lightblue", command=lambda: stock_by_wh(screen)) \
        .grid(row=2, column=1)
    Button(screen, name="stock_by_prod_btn", text="By Products", font=("Ariel", 12),
           width=25, bg="lightblue", command=lambda: stock_by_product(screen)) \
        .grid(row=2, column=3, sticky="w")

    screen.protocol("WM_DELETE_WINDOW", lambda: TkServ.close_and_rem_win_from_opened(screen, "stock"))
    screen.mainloop()
