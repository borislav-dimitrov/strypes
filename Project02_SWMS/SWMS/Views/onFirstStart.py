import Services.tkinterServices as TkServ
import tkinter as tk
import Services.userServices as UserServ


class FirstUser:
    def __init__(self, m_screen, page_name, title, width, height, grid_rows, grid_cols):
        self.m_screen = m_screen
        self.page_name = page_name
        self.width = width
        self.height = height
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.x = (self.m_screen.winfo_screenwidth() / 2) - (self.width / 2)
        self.y = (self.m_screen.winfo_screenheight() / 2) - (self.height / 2)
        self.tmp_user = "asd"
        self.title = title

        self.m_screen.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")
        self.m_screen.resizable(False, False)
        self.m_screen.title(self.title)

        TkServ.setup_grid(self.m_screen, self.width, self.height, self.grid_cols, self.grid_rows)

        self.header_lbl = tk.Label(self.m_screen,
                                   text="No users found.\nCreate the first System account now and remember your password!",
                                   font=("Arial", 15, "bold"))
        self.header_lbl.grid(row=0, column=0, columnspan=5, sticky="we")

        self.uname_lbl = tk.Label(self.m_screen, text="Username", font=("Arial", 12))
        self.uname_lbl.grid(row=1, column=1)

        self.pwd_lbl = tk.Label(self.m_screen, text="Password", font=("Arial", 12))
        self.pwd_lbl.grid(row=2, column=1)

        self.uname_entry = tk.Entry(self.m_screen, width=25, name="system_acc_uname")
        self.uname_entry.grid(row=1, column=2, columnspan=2)

        self.pwd_entry = tk.Entry(self.m_screen, width=25, name="system_acc_pwd", show="*")
        self.pwd_entry.grid(row=2, column=2, columnspan=2)

        self.submit_btn = tk.Button(self.m_screen, text="Register",
                                    font=("Arial", 12), command=lambda: self.register(),
                                    width=15, height=2, name="system_acc_submit")
        self.submit_btn.grid(row=3, column=1, columnspan=3)
        self.m_screen.protocol("WM_DELETE_WINDOW", lambda: self.on_exit())

    def on_exit(self):
        self.tmp_user = "terminate"
        self.m_screen.destroy()

    def register(self):
        # uname = self.m_screen.nametowidget("system_acc_uname")
        # pwd = self.m_screen.nametowidget("system_acc_pwd")
        if len(self.uname_entry.get()) and len(self.pwd_entry.get()) > 1:
            self.tmp_user = {
                "user_id": 1,
                "user_uname": self.uname_entry.get(),
                "user_pwd": UserServ.encrypt_pwd(self.pwd_entry.get()).decode("utf-8"),
                # we are decoding it, so we can store it in the JSON
                "user_type": "Administrator",
                "user_status": "Active",
                "user_last_login": ""
            }
            self.m_screen.destroy()
