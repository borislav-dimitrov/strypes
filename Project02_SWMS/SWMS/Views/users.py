import tkinter
from Services.tkinterServices import setup_grid
from config import *
from Controls.userControls import *


def users_window(m_screen):
    screen = Toplevel(m_screen)
    x = (screen.winfo_screenwidth() / 2) - (RES_WIDTH / 2)
    y = (screen.winfo_screenheight() / 2) - (RES_HEIGHT / 2)
    screen.geometry(f"{RES_WIDTH}x{RES_HEIGHT}+{int(x)}+{int(y)}")
    screen.title("Users")
    setup_grid(screen, RES_WIDTH, RES_HEIGHT, 5, 5)

    Label(screen, name="header_lbl", text="Create/Modify Users", font=("Ariel", 15, "bold")) \
        .grid(row=0, column=2, columnspan=5, sticky="w")

    # Create Buttons
    Button(screen, name="new_usr_btn", text="New", font=("Ariel", 12),
           width=25, bg="lightblue", command=lambda: new_usr(screen)) \
        .grid(row=1, column=1)
    Button(screen, name="edit_usr_btn", text="Edit/Delete", font=("Ariel", 12),
           width=25, bg="lightblue", command=lambda: edit_usr(screen)) \
        .grid(row=1, column=3, sticky="w")

    screen.mainloop()
