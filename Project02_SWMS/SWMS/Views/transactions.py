from tkinter import *
import config as CFG
import Services.tkinterServices as TkServ


def transactions_window(m_screen):
    # Check if another suppliers window is opened
    if "transactions" in CFG.OPENED:
        TkServ.create_custom_msg(m_screen, "Warning!", "Transactions page is already opened!")
        return

    # Add the window to the opened ones
    if "transactions" not in CFG.OPENED:
        CFG.OPENED.append("transactions")

    screen = Toplevel(m_screen)
    x = (screen.winfo_screenwidth() / 2) - (CFG.RES_WIDTH / 2)
    y = (screen.winfo_screenheight() / 2) - (CFG.RES_HEIGHT / 2)
    screen.geometry(f"{CFG.RES_WIDTH}x{CFG.RES_HEIGHT}+{int(x)}+{int(y)}")
    screen.title("Clients")
    TkServ.setup_grid(screen, CFG.RES_WIDTH, CFG.RES_HEIGHT, 5, 10)

    Label(screen, name="header_lbl", text="Transactions", font=("Ariel", 15, "bold")) \
        .grid(row=0, column=2, columnspan=5, sticky="w")

    # Create UI

    screen.protocol("WM_DELETE_WINDOW", lambda: TkServ.close_and_rem_win_from_opened(screen, "transactions"))
    screen.mainloop()
