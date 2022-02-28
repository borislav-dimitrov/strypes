import tkinter as tk
import Services.tkinterServices as TkServ
import Controls.warehouseControls as WhControl
import Models.Db.fakeDB as DB


class Warehouses:
    def __init__(self, m_screen, page_name, title, width, height, grid_rows, grid_cols):
        self.m_screen = m_screen
        self.page_name = page_name
        self.width = width
        self.height = height
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.x = (self.m_screen.winfo_screenwidth() / 2) - (self.width / 2)
        self.y = (self.m_screen.winfo_screenheight() / 2) - (self.height / 2)
        self.title = title

        self.m_screen.geometry(f"{self.width}x{self.height}+{int(self.x) + 15}+{int(self.y) + 30}")
        self.m_screen.title(self.title)

        DB.opened_pages.append(self.page_name)
        TkServ.setup_grid(self.m_screen, self.width, self.height, self.grid_cols, self.grid_rows)

        self.header_lbl = tk.Label(self.m_screen, name="header_lbl", text="Create/Modify Warehouses",
                                   font=("Ariel", 15, "bold"))
        self.header_lbl.grid(row=0, column=2, columnspan=5, sticky="w")

        # Create Buttons
        self.new_btn = tk.Button(self.m_screen, name="new_wh_btn", text="New", font=("Ariel", 12),
                                 width=25, bg="lightblue", command=lambda: self.new_warehouse())
        self.new_btn.grid(row=3, column=1, sticky="w")
        self.edit_btn = tk.Button(self.m_screen, name="edit_wh_btn", text="Edit/Delete", font=("Ariel", 12),
                                  width=25, bg="lightblue", command=lambda: self.edit_warehouse())
        self.edit_btn.grid(row=3, column=5, sticky="w")

        self.m_screen.protocol("WM_DELETE_WINDOW", lambda: self.on_exit())

    def on_exit(self):
        DB.opened_pages.remove(self.page_name)
        self.m_screen.destroy()

    def new_warehouse(self):
        WhControl.new_wh(self.m_screen)

    def edit_warehouse(self):
        WhControl.edit_wh(self.m_screen)


def warehouses_window(m_screen):
    return
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
    screen.title("Warehouses")
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
