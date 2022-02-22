import config as CFG
from tkinter import *
import Services.tkinterServices as TkServ
from Controls.clientControls import new_client, edit_client


def clients_window(m_screen):
    # Check if another suppliers window is opened
    if "clients" in CFG.OPENED:
        TkServ.create_custom_msg(m_screen, "Warning!", "Clients page is already opened!")
        return

    # Add the window to the opened ones
    if "clients" not in CFG.OPENED:
        CFG.OPENED.append("clients")

    screen = Toplevel(m_screen)
    x = (screen.winfo_screenwidth() / 2) - (CFG.RES_WIDTH / 2)
    y = (screen.winfo_screenheight() / 2) - (CFG.RES_HEIGHT / 2)
    screen.geometry(f"{CFG.RES_WIDTH}x{CFG.RES_HEIGHT}+{int(x)}+{int(y)}")
    screen.title("Clients")
    TkServ.setup_grid(screen, CFG.RES_WIDTH, CFG.RES_HEIGHT, 5, 10)

    Label(screen, name="header_lbl", text="Create/Modify Clients", font=("Ariel", 15, "bold")) \
        .grid(row=0, column=2, columnspan=5, sticky="w")

    # Create Buttons
    Button(screen, name="new_client_btn", text="New", font=("Ariel", 12),
           width=25, bg="lightblue", command=lambda: new_client(screen)) \
        .grid(row=1, column=1)
    Button(screen, name="edit_client_btn", text="Edit/Delete", font=("Ariel", 12),
           width=25, bg="lightblue", command=lambda: edit_client(screen)) \
        .grid(row=1, column=3, sticky="w")

    screen.protocol("WM_DELETE_WINDOW", lambda: TkServ.close_and_rem_win_from_opened(screen, "clients"))
    screen.mainloop()

