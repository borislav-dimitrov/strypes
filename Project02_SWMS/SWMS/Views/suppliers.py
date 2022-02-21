from tkinter import *
import config as CFG
import Services.tkinterServices as TkServ
from Controls.supplierControls import new_supplier, edit_supplier


def new_supplier_window(m_screen):
    # Check if another suppliers window is opened
    if "suppliers" in CFG.OPENED:
        TkServ.create_custom_msg(m_screen, "Warning!", "Suppliers page is already opened!")
        return

    # Add the window to the opened ones
    if "suppliers" not in CFG.OPENED:
        CFG.OPENED.append("suppliers")

    screen = Toplevel(m_screen)
    x = (screen.winfo_screenwidth() / 2) - (CFG.RES_WIDTH / 2)
    y = (screen.winfo_screenheight() / 2) - (CFG.RES_HEIGHT / 2)
    screen.geometry(f"{CFG.RES_WIDTH}x{CFG.RES_HEIGHT}+{int(x)}+{int(y)}")
    screen.title("Suppliers")
    TkServ.setup_grid(screen, CFG.RES_WIDTH, CFG.RES_HEIGHT, 5, 10)

    Label(screen, name="header_lbl", text="Create/Modify Suppliers", font=("Ariel", 15, "bold")) \
        .grid(row=0, column=2, columnspan=5, sticky="w")

    # Create Buttons
    Button(screen, name="new_supp_btn", text="New", font=("Ariel", 12),
           width=25, bg="lightblue", command=lambda: new_supplier(screen)) \
        .grid(row=1, column=1)
    Button(screen, name="edit_supp_btn", text="Edit/Delete", font=("Ariel", 12),
           width=25, bg="lightblue", command=lambda: edit_supplier(screen)) \
        .grid(row=1, column=3, sticky="w")

    screen.protocol("WM_DELETE_WINDOW", lambda: TkServ.close_and_rem_win_from_opened(screen, "suppliers"))
    screen.mainloop()
