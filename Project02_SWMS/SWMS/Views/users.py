import tkinter as tk
import Services.tkinterServices as TkServ
import Models.Db.fakeDB as DB
import Controls.userControls as UsrControls


class Users:
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

        self.header_lbl = tk.Label(self.m_screen, name="header_lbl", text="Create/Modify Users",
                                   font=("Ariel", 15, "bold"))
        self.header_lbl.grid(row=0, column=2, columnspan=5, sticky="w")

        # Create Buttons
        self.new_btn = tk.Button(self.m_screen, name="new_usr_btn", text="New", font=("Ariel", 12),
                                 width=25, bg="lightblue", command=lambda: self.new_usr())
        self.new_btn.grid(row=4, column=1)

        self.edit_btn = tk.Button(self.m_screen, name="edit_usr_btn", text="Edit/Delete", font=("Ariel", 12),
                                  width=25, bg="lightblue", command=lambda: self.edit_usr())
        self.edit_btn.grid(row=4, column=5, columnspan=3, sticky="w")

        self.m_screen.protocol("WM_DELETE_WINDOW", lambda: self.on_exit())

    def on_exit(self):
        DB.opened_pages.remove(self.page_name)
        self.m_screen.destroy()

    def new_usr(self):
        UsrControls.new_usr(self.m_screen)

    def edit_usr(self):
        UsrControls.edit_usr(self.m_screen)
