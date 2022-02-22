from tkinter import *
import config as CFG
import Services.tkinterServices as TkServ
from Controls.warehouseControls import new_wh, edit_wh


def warehouses_window(m_screen):
    # Check if another suppliers window is opened
    if "warehouses" in CFG.OPENED:
        TkServ.create_custom_msg(m_screen, "Warning!", "Warehouses page is already opened!")
        return

    # Add the window to the opened ones
    if "warehouses" not in CFG.OPENED:
        CFG.OPENED.append("warehouses")

    screen = Toplevel(m_screen)
    x = (screen.winfo_screenwidth() / 2) - (CFG.RES_WIDTH / 2)
    y = (screen.winfo_screenheight() / 2) - (CFG.RES_HEIGHT / 2)
    screen.geometry(f"{CFG.RES_WIDTH}x{CFG.RES_HEIGHT}+{int(x)}+{int(y)}")
    screen.title("Clients")
    TkServ.setup_grid(screen, CFG.RES_WIDTH, CFG.RES_HEIGHT, 5, 10)

    Label(screen, name="header_lbl", text="Create/Modify Warehouses", font=("Ariel", 15, "bold")) \
        .grid(row=0, column=2, columnspan=5, sticky="w")

    # Create Buttons
    Button(screen, name="new_wh_btn", text="New", font=("Ariel", 12),
           width=25, bg="lightblue", command=lambda: new_wh(screen)) \
        .grid(row=1, column=1)
    Button(screen, name="edit_wh_btn", text="Edit/Delete", font=("Ariel", 12),
           width=25, bg="lightblue", command=lambda: edit_wh(screen)) \
        .grid(row=1, column=3, sticky="w")

    screen.protocol("WM_DELETE_WINDOW", lambda: TkServ.close_and_rem_win_from_opened(screen, "warehouses"))
    screen.mainloop()
