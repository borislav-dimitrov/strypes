import config as CFG
import Services.tkinterServices as TkServ
from tkinter import *
from Controls.salesControls import new_sale


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
    TkServ.setup_grid(screen, CFG.RES_WIDTH, CFG.RES_HEIGHT, 5, 30)

    # Set header
    Label(screen, name="header_lbl", text="Sales", font=("Ariel", 15, "bold")) \
        .grid(row=0, column=2, columnspan=5, sticky="w")

    screen.protocol("WM_DELETE_WINDOW", lambda: TkServ.close_and_rem_win_from_opened(screen, "sell"))
    screen.mainloop()
