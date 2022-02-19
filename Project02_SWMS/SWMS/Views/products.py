from tkinter import *
from config import *
from Services.tkinterServices import setup_grid
from Controls.productControls import new_prod, edit_prod


def products_window(m_screen):
    screen = Toplevel(m_screen)
    x = (screen.winfo_screenwidth() / 2) - (RES_WIDTH / 2)
    y = (screen.winfo_screenheight() / 2) - (RES_HEIGHT / 2)
    screen.geometry(f"{RES_WIDTH}x{RES_HEIGHT}+{int(x)}+{int(y)}")
    screen.title("Products")
    setup_grid(screen, RES_WIDTH, RES_HEIGHT, 5, 10)

    Label(screen, name="header_lbl", text="Create/Modify Products", font=("Ariel", 15, "bold")) \
        .grid(row=0, column=2, columnspan=5, sticky="w")

    # Create Buttons
    Button(screen, name="new_prod_btn", text="New", font=("Ariel", 12),
           width=25, bg="lightblue", command=lambda: new_prod(screen)) \
        .grid(row=1, column=1)
    Button(screen, name="edit_prod_btn", text="Edit/Delete", font=("Ariel", 12),
           width=25, bg="lightblue", command=lambda: edit_prod(screen)) \
        .grid(row=1, column=3, sticky="w")

    screen.mainloop()
